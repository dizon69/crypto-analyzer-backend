# backend/app/collector/ws_collector.py

import asyncio
from collections import deque
import logging
from app.core.binance_ws import BinanceWSClient

logger = logging.getLogger("collector.ws")

class OrderbookCollector:
    def __init__(self, symbols):
        """
        symbols: list, contoh ["btcusdt", "ethusdt", ...]
        """
        self.symbols = symbols
        self.deques = {sym: deque(maxlen=5) for sym in symbols}  # 5 detik terakhir per coin

    def _parse_depth(self, data):
        """
        Ambil best bid/ask dari pesan Binance orderbook update
        """
        stream = data.get('stream', '')
        payload = data.get('data', {})
        if "@depth" in stream and payload:
            symbol = payload.get('s', '').lower()
            bids = payload.get('b', [])
            asks = payload.get('a', [])
            # Top 5 bid/ask → sum qty
            sum_bids = sum(float(b[1]) for b in bids[:5])
            sum_asks = sum(float(a[1]) for a in asks[:5])
            ts = payload.get('T', 0)  # event time ms
            return symbol, sum_bids, sum_asks, ts
        return None

    def on_orderbook_update(self, data):
        res = self._parse_depth(data)
        if not res:
            return
        symbol, sum_bids, sum_asks, ts = res
        if symbol in self.deques:
            ratio = (sum_bids / sum_asks) if sum_asks > 0 else 0
            self.deques[symbol].append({
                "ratio": ratio,
                "sum_bids": sum_bids,
                "sum_asks": sum_asks,
                "ts": ts
            })
            logger.debug(f"[{symbol}] buy/sell={ratio:.2f} bids={sum_bids:.2f} asks={sum_asks:.2f}")

    def get_last_n(self, symbol, n=5):
        dq = self.deques.get(symbol)
        return list(dq)[-n:] if dq else []

    def get_all(self):
        return {sym: list(dq) for sym, dq in self.deques.items()}


class KlineCollector:
    def __init__(self, symbols):
        self.symbols = symbols
        self.klines = {sym: deque(maxlen=6) for sym in symbols}

    def _parse_kline(self, data):
        stream = data.get('stream', '')
        payload = data.get('data', {})
        if "@kline_1h" in stream and payload:
            symbol = payload.get('s', '').lower()
            kline = payload.get('k', {})
            close_time = kline.get('T')
            close = float(kline.get('c'))
            volume = float(kline.get('v'))
            is_closed = kline.get('x', False)
            return symbol, close, volume, close_time, is_closed
        return None

    def on_kline_update(self, data):
        res = self._parse_kline(data)
        if not res:
            return
        symbol, close, volume, close_time, is_closed = res
        if symbol in self.klines and is_closed:
            self.klines[symbol].append({
                "close_time": close_time,
                "close": close,
                "volume": volume,
            })

    def get_last_n(self, symbol, n=3):
        dq = self.klines.get(symbol)
        return list(dq)[-n:] if dq else []

    def get_all(self):
        return {sym: list(dq) for sym, dq in self.klines.items()}


# ================== Run background task BinanceWSClient + Collector ==================
async def start_collector(symbols):
    orderbook_streams = [f"{s}@depth5@100ms" for s in symbols]
    kline_streams = [f"{s}@kline_1h" for s in symbols]
    streams = orderbook_streams + kline_streams

    orderbook_collector = OrderbookCollector(symbols)
    kline_collector = KlineCollector(symbols)

    def on_message(data):
        orderbook_collector.on_orderbook_update(data)
        kline_collector.on_kline_update(data)

    ws_client = BinanceWSClient(streams, on_message)
    asyncio.create_task(ws_client.run())
    return orderbook_collector, kline_collector

# ============ USAGE EXAMPLE ============
if __name__ == "__main__":
    import time

    symbols = ["btcusdt", "ethusdt", "solusdt"]
    collector, kline_collector = None, None

    async def main():
        global collector, kline_collector
        collector, kline_collector = await start_collector(symbols)
        while True:
            print("Orderbook:", collector.get_all())
            print("Kline:", kline_collector.get_all())
            await asyncio.sleep(1)

    asyncio.run(main())
