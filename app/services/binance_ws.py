import asyncio
import json
import websockets
from app.core.buyqueue_logic import BuySellRatioTracker

tracker = BuySellRatioTracker()

async def start_binance_ws():
    url = "wss://stream.binance.com:9443/ws"
    pairs = ["btcusdt", "ethusdt", "solusdt", "bnbusdt", "adausdt",
             "xrpusdt", "ltcusdt", "dogeusdt", "linkusdt", "avaxusdt"]
    streams = [f"{pair}@depth5@100ms" for pair in pairs]

    payload = {
        "method": "SUBSCRIBE",
        "params": streams,
        "id": 1
    }

    async with websockets.connect(url, ping_interval=20, ping_timeout=60) as ws:
        await ws.send(json.dumps(payload))
        async for message in ws:
            data = json.loads(message)
            if not ("b" in data and "a" in data and "s" in data):
                continue
            symbol = data["s"].lower()
            try:
                buy_qty = sum(float(x[1]) for x in data["b"])
                sell_qty = sum(float(x[1]) for x in data["a"])
                tracker.update(symbol, buy_qty, sell_qty)
            except Exception:
                continue

def get_top_buyqueue():
    return tracker.get_top()