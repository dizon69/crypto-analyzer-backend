from collections import deque
import time

class BuySellRatioTracker:
    def __init__(self):
        self.data = {}

    def update(self, symbol, buy, sell):
        now = time.time()
        dq = self.data.setdefault(symbol, deque(maxlen=4))
        dq.append((now, buy, sell))

    def get_top(self, limit=10):
        result = []
        for symbol, entries in self.data.items():
            if len(entries) < 3:
                continue

            buy_avg = sum(x[1] for x in entries) / len(entries)
            sell_avg = sum(x[2] for x in entries) / len(entries)
            ratio = buy_avg / sell_avg if sell_avg > 0 else 0

            total = buy_avg + sell_avg
            result.append({
                "symbol": symbol.upper(),
                "buy_ratio": round((buy_avg / total) * 100, 1),
                "sell_ratio": round((sell_avg / total) * 100, 1)
            })

        return sorted(result, key=lambda x: x["buy_ratio"], reverse=True)[:limit]
