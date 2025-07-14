import asyncio
import json
import websockets

from logic.buyqueue import tracker

PAIRS = [
    "btcusdt", "ethusdt", "solusdt", "bnbusdt", "adausdt", 
    "xrpusdt", "ltcusdt", "dogeusdt", "linkusdt", "avaxusdt"
]

async def run_binance_ws():
    print("Start script...")  # DEBUG 1
    stream_list = [f"{pair}@depth5@100ms" for pair in PAIRS]
    payload = {
        "method": "SUBSCRIBE",
        "params": stream_list,
        "id": 1
    }
    url = "wss://stream.binance.com:9443/ws"
    try:
        async with websockets.connect(url, ping_interval=20, ping_timeout=60) as ws:
            print("WS Connected!")  # DEBUG 2
            await ws.send(json.dumps(payload))
            print("SUBSCRIBE sent!")  # DEBUG 3
            async for msg in ws:
                print("DATA MASUK MANA??", msg)  # DEBUG 4
                data = json.loads(msg)
                if not all(k in data for k in ("s", "b", "a")):
                    continue
                symbol = data["s"].lower()
                buy_qty = sum(float(x[1]) for x in data["b"])
                sell_qty = sum(float(x[1]) for x in data["a"])
                tracker.update(symbol, buy_qty, sell_qty)
    except Exception as e:
        print("ERROR:", e)  # DEBUG ERROR

if __name__ == "__main__":
    asyncio.run(run_binance_ws())
