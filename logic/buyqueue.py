from collections import deque
import time

class BuySellRatioTracker:
    def __init__(self):
        self.data = {}

    def update(self, symbol: str, buy_qty: float, sell_qty: float):
        now = time.time()
        dq = self.data.setdefault(symbol, deque(maxlen=5))
        dq.append((now, buy_qty, sell_qty))

    def get_top_buy_ratio(self, min_ratio=1.6, limit=10):
        result = []
        for symbol, entries in self.data.items():
            if len(entries) < 5:
                continue
            buy_avg = sum(x[1] for x in entries) / len(entries)
            sell_avg = sum(x[2] for x in entries) / len(entries)
            ratio = buy_avg / (sell_avg + 1e-9)
            if ratio >= min_ratio:
                result.append({
                    "symbol": symbol.upper(),
                    "buy": round(buy_avg, 2),
                    "sell": round(sell_avg, 2),
                    "ratio": round(ratio, 2)
                })
        return sorted(result, key=lambda x: x["ratio"], reverse=True)[:limit]

# Singleton
tracker = BuySellRatioTracker()
