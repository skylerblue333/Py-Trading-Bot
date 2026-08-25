from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from decimal import Decimal
from typing import Literal

Signal = Literal["BUY", "SELL", "HOLD"]


@dataclass(frozen=True)
class Trade:
    step: int
    side: Literal["BUY", "SELL"]
    price: Decimal
    quantity: int


@dataclass(frozen=True)
class BacktestResult:
    starting_cash: Decimal
    ending_cash: Decimal
    ending_position: int
    ending_value: Decimal
    trades: tuple[Trade, ...]


class PaperTrader:
    """Deterministic, single-asset paper-trading/backtest engine.

    This class never contacts a broker or market-data provider and never places
    real orders. Prices are caller supplied.
    """

    def __init__(
        self,
        initial_cash: Decimal = Decimal("10000.00"),
        short_window: int = 3,
        long_window: int = 5,
        max_position: int = 1,
    ) -> None:
        if initial_cash <= 0:
            raise ValueError("initial_cash must be positive")
        if short_window < 1 or long_window <= short_window:
            raise ValueError("require 1 <= short_window < long_window")
        if max_position < 1:
            raise ValueError("max_position must be positive")
        self.initial_cash = initial_cash
        self.short_window = short_window
        self.long_window = long_window
        self.max_position = max_position

    def signal(self, prices: list[Decimal]) -> Signal:
        if len(prices) < self.long_window:
            return "HOLD"
        short_avg = sum(prices[-self.short_window :], Decimal(0)) / self.short_window
        long_avg = sum(prices[-self.long_window :], Decimal(0)) / self.long_window
        if short_avg > long_avg:
            return "BUY"
        if short_avg < long_avg:
            return "SELL"
        return "HOLD"

    def run(self, prices: Iterable[Decimal]) -> BacktestResult:
        series = list(prices)
        if not series:
            raise ValueError("at least one price is required")
        if len(series) > 100_000:
            raise ValueError("price series exceeds 100000 observations")
        if any(price <= 0 for price in series):
            raise ValueError("prices must be positive")

        cash = self.initial_cash
        position = 0
        observed: list[Decimal] = []
        trades: list[Trade] = []

        for step, price in enumerate(series):
            observed.append(price)
            action = self.signal(observed)
            if action == "BUY" and position < self.max_position and cash >= price:
                cash -= price
                position += 1
                trades.append(Trade(step, "BUY", price, 1))
            elif action == "SELL" and position > 0:
                cash += price
                position -= 1
                trades.append(Trade(step, "SELL", price, 1))

        ending_value = cash + Decimal(position) * series[-1]
        return BacktestResult(
            starting_cash=self.initial_cash,
            ending_cash=cash,
            ending_position=position,
            ending_value=ending_value,
            trades=tuple(trades),
        )


def demo() -> None:
    prices = [Decimal(value) for value in ("100", "99", "98", "101", "104", "106", "103", "100")]
    result = PaperTrader().run(prices)
    print(
        {
            "mode": "paper-only",
            "ending_value": str(result.ending_value),
            "ending_position": result.ending_position,
            "trades": len(result.trades),
        }
    )


if __name__ == "__main__":
    demo()
