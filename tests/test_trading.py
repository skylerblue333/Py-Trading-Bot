from decimal import Decimal

import pytest

from main import PaperTrader


def prices(*values: str) -> list[Decimal]:
    return [Decimal(value) for value in values]


def test_requires_valid_configuration() -> None:
    with pytest.raises(ValueError):
        PaperTrader(initial_cash=Decimal("0"))
    with pytest.raises(ValueError):
        PaperTrader(short_window=5, long_window=5)


def test_rejects_empty_or_non_positive_prices() -> None:
    trader = PaperTrader()
    with pytest.raises(ValueError):
        trader.run([])
    with pytest.raises(ValueError):
        trader.run(prices("100", "0"))


def test_strategy_is_deterministic_and_bounded() -> None:
    trader = PaperTrader(initial_cash=Decimal("1000"), short_window=2, long_window=3, max_position=1)
    result = trader.run(prices("100", "99", "101", "104", "103", "98", "97"))
    assert result.trades
    assert all(trade.quantity == 1 for trade in result.trades)
    assert result.ending_position in (0, 1)
    assert result.ending_value == result.ending_cash + Decimal(result.ending_position) * Decimal("97")


def test_never_buys_without_cash() -> None:
    trader = PaperTrader(initial_cash=Decimal("50"), short_window=1, long_window=2)
    result = trader.run(prices("100", "101", "102"))
    assert result.trades == ()
    assert result.ending_cash == Decimal("50")
