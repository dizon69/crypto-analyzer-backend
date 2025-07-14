import asyncio
import json
import websockets

PAIRS = [
    "btcusdt", "ethusdt", "solusdt", "bnbusdt", "adausdt", 
    "xrpusdt", "ltcusdt", "dogeusdt", "linkusdt", "avaxusdt"
]

async def run_binance_ws():
    url = "wss://stream.binance.com:9443/ws"
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
            # Print hanya data WS yang BENAR
            if "e" in data and "b" in data and "a" in data and "s" in data:
                print("✅ DATA WS BENAR:", data)
            else:
                print("❌ DATA BUKAN WS YG DIHARAPKAN:", data)

if __name__ == "__main__":
    asyncio.run(run_binance_ws())
