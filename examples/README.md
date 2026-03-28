# Examples

Runnable example scripts for the `kiwoom-rest-api` library.
All scripts use `is_mock=True` and connect to the Kiwoom mock trading server.

## Prerequisites

Set your credentials as environment variables:

```bash
export KIWOOM_APP_KEY="your_app_key"
export KIWOOM_APP_SECRET="your_app_secret"
export KIWOOM_ACCOUNT_NO="your_account_number"  # required for account/order examples
```

## Scripts

### `basic_usage.py`

Login, fetch basic stock info for Samsung Electronics (005930), query account evaluation, then logout.

```bash
uv run python examples/basic_usage.py
```

### `market_data.py`

Fetch stock quote (호가), daily chart, top volume ranking, and all sector index.

```bash
uv run python examples/market_data.py
```

### `trading.py`

Place a buy order, a sell order, modify the buy order price, then cancel the sell order.

```bash
uv run python examples/trading.py
```

### `realtime_websocket.py`

Connect via WebSocket and subscribe to real-time execution data (0B 주식체결) and order book
data (0D 주식호가잔량) for multiple stocks. Listens for 30 seconds then exits.

```bash
uv run python examples/realtime_websocket.py
```
