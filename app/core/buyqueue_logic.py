from collections import deque
import time

MAXLEN = 5
MIN_BUY_SELL_RATIO = 1.6

class BuyQueueAnalyzer:
    def __init__(self):
        self.coin_data = {}

    def update_coin(self, symbol, buy_qty, sell_qty):
        ratio = buy_qty / sell_qty if sell_qty > 0 else 0
        dq = self.coin_data.setdefault(symbol, deque(maxlen=MAXLEN))
        dq.append((time.time(), ratio))

    def get_top_buyers(self):
        result = []
        for symbol, entries in self.coin_data.items():
            if len(entries) < MAXLEN:
                continue
            ratios = [r for _, r in entries]
            if all(r > MIN_BUY_SELL_RATIO for r in ratios) and not self.too_fluctuating(ratios):
                avg_ratio = sum(ratios) / len(ratios)
                result.append((symbol, avg_ratio))
        return sorted(result, key=lambda x: x[1], reverse=True)[:10]

    def too_fluctuating(self, ratios):
        return max(ratios) - min(ratios) > 1.0
