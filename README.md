# Sky Paper Trader

**Status: engineering beta / simulation only.**

Sky Paper Trader is a deterministic single-asset backtest primitive for the SKYCOIN4444 engineering lab. It evaluates caller-supplied prices with a simple moving-average crossover rule and records simulated whole-unit trades using decimal arithmetic.

## What it does

- deterministic short/long moving-average signals
- bounded price-series input (100,000 observations)
- configurable starting cash, windows, and maximum position
- simulated BUY/SELL decisions with cash and position constraints
- reproducible trade ledger and mark-to-market ending value
- unit tests, Ruff, compile checks, dependency audit, Docker build, non-root image verification, and container smoke test in CI

## What it does not do

This repository does **not** connect to a broker or exchange, submit orders, fetch live market data, provide investment advice, predict returns, manage real funds, or claim profitable/production trading. Slippage, fees, liquidity, corporate actions, latency, taxes, and many other market effects are not modeled.

## Run

```bash
python main.py
```

The bundled demo uses static sample prices and prints a summary with `mode: paper-only`.

## Test

```bash
python -m pip install -r requirements.txt
ruff check main.py tests
pytest -q
pip-audit -r requirements.txt
```

## Integration

SKYCOIN4444 can consume this component as an offline strategy-simulation boundary. Any future live-market or brokerage adapter must be isolated, explicitly configured, independently secured, and separately verified.
