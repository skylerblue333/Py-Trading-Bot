from dataclasses import dataclass
from typing import List

@dataclass
class Candle:
    close: float

def simple_moving_average(candles: List[Candle], period: int) -> float:
    if len(candles) < period:
        raise ValueError(f"Need at least {period} candles, got {len(candles)}")
    return sum(c.close for c in candles[-period:]) / period

def rsi(candles: List[Candle], period: int = 14) -> float:
    if len(candles) < period + 1:
        raise ValueError("Not enough data for RSI")
    gains, losses = [], []
    for i in range(1, period + 1):
        delta = candles[-i].close - candles[-(i+1)].close
        if delta >= 0:
            gains.append(delta)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(abs(delta))
    avg_gain = sum(gains) / period
    avg_loss = sum(losses) / period
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def signal(candles: List[Candle], fast: int = 9, slow: int = 21) -> str:
    if len(candles) < slow:
        return "HOLD"
    fast_ma = simple_moving_average(candles, fast)
    slow_ma = simple_moving_average(candles, slow)
    if fast_ma > slow_ma:
        return "BUY"
    elif fast_ma < slow_ma:
        return "SELL"
    return "HOLD"
