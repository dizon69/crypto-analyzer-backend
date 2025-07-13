from collections import deque
import time

class BuySellRatioTracker:
    def __init__(self):
        self.data = {}  # {symbol: deque of (timestamp, buy_qty, sell_qty)}

    def update(self, symbol, buy, sell):
        now = time.time()
        dq = self.data.setdefault(symbol, deque(maxlen=5))  # 🟢 cukup 4 data aja
        dq.append((now, buy, sell))

    def get_top(self):
        result = []
        for symbol, entries in self.data.items():
            if len(entries) < 3:  # 🟢 sebelumnya 5, sekarang cukup 3
                continue

            buy_avg = sum(x[1] for x in entries) / len(entries)
            sell_avg = sum(x[2] for x in entries) / len(entries)
            ratio = buy_avg / sell_avg if sell_avg > 0 else 0

            if ratio < 1.3:
                continue

            if self.too_fluctuating(entries):
                continue  # ❗️masih dicek tapi boleh di-nonaktif kalau mau

            total = buy_avg + sell_avg
            result.append({
                "symbol": symbol.upper(),
                "buy": round((buy_avg / total) * 100, 1),
                "sell": round((sell_avg / total) * 100, 1)
            })

        return sorted(result, key=lambda x: x["buy"], reverse=True)[:10]

    def too_fluctuating(self, entries):
        ratios = [b / s if s > 0 else 0 for _, b, s in entries]
        return max(ratios) - min(ratios) > 1.4  # 🟢 sebelumnya > 1.0 → sekarang 1.4
