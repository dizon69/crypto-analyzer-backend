import asyncio
import json
import websockets

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

            # Untuk multi-stream, data dikirim di key 'stream' dan 'data'
            if "stream" in data and "data" in data:
                symbol = data["stream"].split("@")[0]
                bids = data["data"]["bids"]
                asks = data["data"]["asks"]
                buy_qty = sum(float(bid[1]) for bid in bids)
                sell_qty = sum(float(ask[1]) for ask in asks)
                print(f"SYMBOL: {symbol} | BUY: {buy_qty} | SELL: {sell_qty}")
            else:
                print("Bukan format multi-stream:", data)

if __name__ == "__main__":
    asyncio.run(run_binance_ws())
