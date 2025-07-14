import asyncio
import json
import websockets
from logic.buyqueue import tracker  # pastikan tracker ini sudah ada!

PAIRS = [
    "btcusdt", "ethusdt", "solusdt", "bnbusdt", "adausdt", 
    "xrpusdt", "ltcusdt", "dogeusdt", "linkusdt", "avaxusdt"
]

async def run_binance_ws():
    url = "wss://stream.binance.com:9443/stream"
    streams = [f"{pair}@depth5@100ms" for pair in PAIRS]
    payload = {
        "method": "SUBSCRIBE",
        "params": streams,
        "id": 1
    }

    async with websockets.connect(url, ping_interval=20, ping_timeout=60) as ws:
        await ws.send(json.dumps(payload))
        while True:
            msg = await ws.recv()
            data = json.loads(msg)

            if "stream" in data and "data" in data:
                symbol = data["stream"].split("@")[0]
                bids = data["data"]["bids"]
                asks = data["data"]["asks"]
                buy_qty = sum(float(bid[1]) for bid in bids)
                sell_qty = sum(float(ask[1]) for ask in asks)
                # Update ke tracker logic kamu!
                tracker.update(symbol, buy_qty, sell_qty)
            else:
                print("Bukan format multi-stream:", data)

if __name__ == "__main__":
    asyncio.run(run_binance_ws())
