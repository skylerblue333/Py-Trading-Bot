"""Backtesting-oriented strategy scaffold; no live trading is enabled by default."""
import pandas as pd

def moving_average_signal(prices: pd.Series, fast: int = 20, slow: int = 50) -> pd.Series:
    fast_ma = prices.rolling(fast).mean()
    slow_ma = prices.rolling(slow).mean()
    return (fast_ma > slow_ma).astype(int).diff().fillna(0)

if __name__ == "__main__":
    prices = pd.Series([100 + i * 0.5 for i in range(100)])
    print(moving_average_signal(prices).tail())
