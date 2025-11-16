from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List
import numpy as np

app = FastAPI()
templates = Jinja2Templates(directory="templates")


class Sale(BaseModel):
    date: str
    amount: float


class ForecastRequest(BaseModel):
    sales: List[Sale]


@app.get("/")
def home():
    return {"message": "Bienvenue sur l'API Vente Visible Forecast"}


@app.post("/forecast")
def forecast_sales(data: ForecastRequest):
    if len(data.sales) < 2:
        return {"error": "Au moins 2 ventes sont nécessaires pour prévoir la suivante."}
    
    amounts = [s.amount for s in data.sales]
    avg = np.mean(amounts)

    forecast = {
        "next_month_1": avg * 1.05,
        "next_month_2": avg * 1.1,
        "next_month_3": avg * 1.15,
    }
    return forecast


@app.get("/form", response_class=HTMLResponse)
def get_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})


@app.post("/form", response_class=HTMLResponse)
async def submit_form(request: Request, 
                      date1: str = Form(...), amount1: float = Form(...),
                      date2: str = Form(...), amount2: float = Form(...),
                      date3: str = Form(...), amount3: float = Form(...)):
    
    sales_data = {
        "sales": [
            {"date": date1, "amount": amount1},
            {"date": date2, "amount": amount2},
            {"date": date3, "amount": amount3},
        ]
    }

    amounts = [amount1, amount2, amount3]
    avg = np.mean(amounts)

    forecast = {
        "next_month_1": round(avg * 1.05, 2),
        "next_month_2": round(avg * 1.10, 2),
        "next_month_3": round(avg * 1.15, 2),
    }

    return templates.TemplateResponse("form.html", {
        "request": request,
        "forecast": forecast
    })
