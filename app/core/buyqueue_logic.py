from collections import deque
import time

class BuySellRatioTracker:
    def __init__(self):
        self.data = {}  # {symbol: (buy_qty, sell_qty, timestamp)}

    def update(self, symbol, buy, sell):
        self.data[symbol] = {
            "symbol": symbol.upper(),
            "buy_qty": round(buy, 2),
            "sell_qty": round(sell, 2),
            "timestamp": time.time()
        }

    def get_latest(self):
        return list(self.data.values())
