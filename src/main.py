from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from src.strategy import Candle, signal, rsi, simple_moving_average

app = FastAPI(title="Trading Bot API")

class PriceData(BaseModel):
    prices: List[float]

@app.post("/signal")
def get_signal(data: PriceData):
    candles = [Candle(close=p) for p in data.prices]
    s = signal(candles)
    r = rsi(candles) if len(candles) >= 15 else None
    return {"signal": s, "rsi": r}

@app.get("/health")
def health():
    return {"status": "ok"}
