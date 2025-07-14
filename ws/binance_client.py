### ws/binance_client.py
import asyncio
import json
import websockets
from logic.buyqueue import BuySellRatioTracker
from config import PAIRS

tracker = BuySellRatioTracker()

async def run_binance_ws():
    stream_list = [f"{pair}@depth5@100ms" for pair in PAIRS]
    payload = {
        "method": "SUBSCRIBE",
        "params": stream_list,
        "id": 1
    }
    url = "wss://stream.binance.com:9443/ws"

    async with websockets.connect(url, ping_interval=20, ping_timeout=60) as ws:
        await ws.send(json.dumps(payload))
        async for msg in ws:
            data = json.loads(msg)
            if not all(k in data for k in ("s", "b", "a")):
                continue
            symbol = data["s"].lower()
            buy_qty = sum(float(x[1]) for x in data["b"])
            sell_qty = sum(float(x[1]) for x in data["a"])
            tracker.update(symbol, buy_qty, sell_qty)