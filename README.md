# Py-Trading-Bot

Algorithmic trading signal engine with SMA crossover and RSI indicators.

## Quick Start

```bash
pip install -r requirements.txt
pytest tests/ -v
uvicorn src.main:app --reload
```

## API

`POST /signal` with `{"prices": [100, 101, 99, ...]}`  
Returns `{"signal": "BUY"|"SELL"|"HOLD", "rsi": 55.2}`
