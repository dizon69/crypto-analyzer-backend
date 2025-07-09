import asyncio
from app.services.binance_ws import BinanceOrderbookWS

SYMBOLS = [
    "btcusdt", "ethusdt", "bnbusdt", "solusdt", "adausdt",
    "xrpusdt", "dogeusdt", "maticusdt", "ltcusdt", "linkusdt"
]

orderbook_data = {}  # {symbol: [ {time, buy, sell}, ... ] }

async def start_binance_listener():
    async for symbol, bids, asks in BinanceOrderbookWS(SYMBOLS):
        now = int(asyncio.get_event_loop().time() * 1000)
        total_buy = sum(float(price) * float(qty) for price, qty in bids)
        total_sell = sum(float(price) * float(qty) for price, qty in asks)
        entry = {"time": now, "buy": total_buy, "sell": total_sell}
        if symbol not in orderbook_data:
            orderbook_data[symbol] = []
        orderbook_data[symbol].append(entry)
        # Keep only last 5 menit (300.000 ms)
        orderbook_data[symbol] = [
            d for d in orderbook_data[symbol] if now - d["time"] <= 300000
        ][:300]
