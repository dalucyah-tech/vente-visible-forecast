from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import numpy as np

app = FastAPI()

class Sale(BaseModel):
    date: str
    amount: float

class ForecastRequest(BaseModel):
    sales: List[Sale]

@app.post("/forecast")
def forecast_sales(data: ForecastRequest):
    if len(data.sales) < 3:
        return {"error": "Not enough data"}
    
    amounts = [s.amount for s in data.sales]
    avg = np.mean(amounts[-3:])
    
    forecast = {
        "next_month_1": round(avg * 1.03, 2),
        "next_month_2": round(avg * 1.06, 2),
        "next_month_3": round(avg * 1.09, 2),
    }

    return {"forecast": forecast}
