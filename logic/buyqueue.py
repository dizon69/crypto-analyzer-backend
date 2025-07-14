# logic/buyqueue.py
from collections import deque
import time

class BuySellRatioTracker:
    def __init__(self):
        self.data = {}  # symbol -> deque

    def update(self, symbol: str, buy_qty: float, sell_qty: float):
        now = time.time()
        dq = self.data.setdefault(symbol, deque(maxlen=5))
        dq.append((now, buy_qty, sell_qty))

    def get_top_buy_ratio(self, min_ratio=1.6, limit=10, min_data=1):  # <- Tambahin min_data param
        result = []
        for symbol, entries in self.data.items():
            if len(entries) < min_data:      # <- Default minimal 1 data biar langsung tampil
                continue

            # Kalau data < 5, skip pengecekan "stable"
            if len(entries) >= 5:
                stable = all(
                    abs(entries[i][1] / (entries[i][2] + 1e-9) - entries[0][1] / (entries[0][2] + 1e-9)) < 0.5
                    for i in range(1, 5)
                )
                if not stable:
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
