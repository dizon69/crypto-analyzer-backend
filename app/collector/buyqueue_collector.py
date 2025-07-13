import asyncio
import json
import websockets
from app.core.globals import tracker

async def collect():
    print("🔌 Connecting to Binance WebSocket...")
    url = "wss://stream.binance.com:9443/ws"
    pairs = ["btcusdt", "ethusdt", "solusdt", "bnbusdt", "adausdt", "xrpusdt", "ltcusdt", "dogeusdt", "linkusdt", "avaxusdt"]
    streams = [f"{pair}@depth5@100ms" for pair in pairs]

    payload = {
        "method": "SUBSCRIBE",
        "params": streams,
        "id": 1
    }

    cache = {}

    async with websockets.connect(url, ping_interval=20, ping_timeout=60) as ws:
        await ws.send(json.dumps(payload))
        print("✅ Subscribed to Binance streams")

        async for message in ws:
            data = json.loads(message)
            if not ("b" in data and "a" in data and "s" in data):
                continue

            symbol = data["s"].upper()
            try:
                buy_qty = sum(float(x[1]) for x in data["b"])
                sell_qty = sum(float(x[1]) for x in data["a"])
                total = buy_qty + sell_qty
                if total == 0:
                    continue

                buy_ratio = round((buy_qty / total) * 100, 2)
                sell_ratio = round((sell_qty / total) * 100, 2)

                cache[symbol] = {
                    "symbol": symbol,
                    "buy_qty": buy_qty,
                    "sell_qty": sell_qty,
                    "buy_ratio": buy_ratio,
                    "sell_ratio": sell_ratio
                }

                # Update tracker tiap minimal 5 coin terkumpul
                if len(cache) >= 5:
                    tracker.update(list(cache.values()))
                    cache.clear()

            except Exception as e:
                print(f"⚠️ Error on {symbol}: {e}")

def get_top_buy_queue():
    return tracker.get_top()
