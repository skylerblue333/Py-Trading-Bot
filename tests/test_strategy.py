from src.strategy import Candle, simple_moving_average, rsi, signal

def make_candles(prices):
    return [Candle(close=p) for p in prices]

def test_sma():
    candles = make_candles([10, 20, 30])
    assert simple_moving_average(candles, 3) == 20.0

def test_sma_period():
    candles = make_candles([10, 20, 30, 40])
    assert simple_moving_average(candles, 2) == 35.0

def test_signal_buy():
    # Fast MA > Slow MA => BUY
    prices = list(range(1, 30)) + [100, 110, 120]
    candles = make_candles(prices)
    assert signal(candles, fast=5, slow=21) == "BUY"

def test_signal_hold_insufficient_data():
    candles = make_candles([10, 20])
    assert signal(candles) == "HOLD"
