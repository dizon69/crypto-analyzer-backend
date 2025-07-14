import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
import json
import websockets
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
    url = "wss://stream.binance.com:9443/ws"

    async with websockets.connect(url, ping_interval=20, ping_timeout=60) as ws:
        await ws.send(json.dumps(payload))
        print("🔥 SUBSCRIBE SENT, WAITING DATA ...", flush=True)
        async for msg in ws:
            data = json.loads(msg)
            if 'result' in data:  # Ini cuma response subscribe, skip aja
                continue
            if not all(k in data for k in ("s", "b", "a")):
                print("DATA WS BUKAN FORMAT DIHARAPKAN:", data, flush=True)
                continue
            symbol = data["s"].lower()
            buy_qty = sum(float(x[1]) for x in data["b"])
            sell_qty = sum(float(x[1]) for x in data["a"])
            print(f"SYMBOL: {symbol} | BUY: {buy_qty} | SELL: {sell_qty}", flush=True)
            tracker.update(symbol, buy_qty, sell_qty)

if __name__ == "__main__":
    asyncio.run(run_binance_ws())
