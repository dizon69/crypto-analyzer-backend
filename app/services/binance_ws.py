import asyncio
import websockets
import json
import random

class BinanceOrderbookWS:
    BASE_URL = "wss://stream.binance.com:9443/stream"
    def __init__(self, symbols):
        self.symbols = symbols

    async def __aiter__(self):
        streams = '/'.join(f'{s}@depth10@100ms' for s in self.symbols)
        url = f"{self.BASE_URL}?streams={streams}"
        while True:
            try:
                async with websockets.connect(url, ping_interval=20, ping_timeout=60) as ws:
                    async for msg in ws:
                        data = json.loads(msg)
                        stream = data['stream']
                        symbol = stream.split("@")[0]
                        bids = data['data']['bids']
                        asks = data['data']['asks']
                        yield symbol, bids, asks
            except Exception as e:
                print("Binance WS Error:", e)
                await asyncio.sleep(5 + random.uniform(0, 5))  # random delay reconnect 5-10 detik
