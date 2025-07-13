import asyncio
import json
import websockets
from buyqueue_logic import BuyQueueAnalyzer

analyzer = BuyQueueAnalyzer()

async def collect_data():
    stream_url = "wss://stream.binance.com:9443/ws"
    symbols = ["btcusdt", "ethusdt", "solusdt", "bnbusdt", "adausdt", "linkusdt", "dogeusdt", "avaxusdt", "maticusdt", "xrpusdt"]
    params = [f"{s}@depth" for s in symbols]
    stream_payload = {
        "method": "SUBSCRIBE",
        "params": params,
        "id": 1
    }

    async with websockets.connect(stream_url, ping_interval=20, ping_timeout=60) as ws:
        await ws.send(json.dumps(stream_payload))
        async for msg in ws:
            data = json.loads(msg)
            if 'b' in data and 'a' in data:
                bids = float(data['b'][0][1])
                asks = float(data['a'][0][1])
                symbol = data['s'].lower()
                analyzer.update_coin(symbol, bids, asks)

def get_top_buy_data():
    return analyzer.get_top_buyers()
