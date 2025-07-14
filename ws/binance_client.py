import sys
import os
import asyncio
import json
import websockets

# Agar bisa import logic.buyqueue walau di folder ws/
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
from logic.buyqueue import tracker

PAIRS = [
    "btcusdt", "ethusdt", "solusdt", "bnbusdt", "adausdt",
    "xrpusdt", "ltcusdt", "dogeusdt", "linkusdt", "avaxusdt"
]

async def run_binance_ws():
    stream_list = [f"{pair}@depth5@100ms" for pair in PAIRS]
    payload = {
        "method": "SUBSCRIBE",
        "params": stream_list,
        "id": 1
    }
    url = "wss://stream.binance.com:9443/stream"  # <--- PENTING
    async with websockets.connect(url, ping_interval=20, ping_timeout=60) as ws:
        await ws.send(json.dumps(payload))
        while True:
            msg = await ws.recv()
            data = json.loads(msg)
            # Hanya proses kalau key-nya ada 'data' (multi stream)
            if not isinstance(data, dict) or "data" not in data:
                continue
            d = data["data"]
            if not all(k in d for k in ("s", "b", "a")):
                continue
            symbol = d["s"].lower()
            buy_qty = sum(float(x[1]) for x in d["b"])
            sell_qty = sum(float(x[1]) for x in d["a"])
            tracker.update(symbol, buy_qty, sell_qty)
            print(f"SYMBOL: {symbol} | BUY: {buy_qty} | SELL: {sell_qty}")

if __name__ == "__main__":
    asyncio.run(run_binance_ws())
