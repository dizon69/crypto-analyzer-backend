from collections import deque
import time

class BuySellRatioTracker:
    def __init__(self):
        self.data = {}

    def update(self, result: list[dict]):
        for entry in result:
            symbol = entry["symbol"]
            self.data[symbol] = entry

    def get_top(self, limit=10):
        # Balikin list top coin berdasarkan rasio buy tertinggi
        sorted_data = sorted(
            self.data.values(),
            key=lambda x: x["buy_ratio"],
            reverse=True
        )
        return sorted_data[:limit]
