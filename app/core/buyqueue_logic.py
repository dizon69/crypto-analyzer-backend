import time
from collections import deque

# === Parameter ===
MAXLEN = 5
RATIO_THRESHOLD = 1.6

class BuyQueueAnalyzer:
    def __init__(self, symbols):
        self.symbols = symbols
        self.data = {sym: deque(maxlen=MAXLEN) for sym in symbols}

    def update(self, symbol, ratio, sum_bids, sum_asks, ts):
        if symbol not in self.data:
            return
        self.data[symbol].append({
            "ratio": ratio,
            "sum_bids": sum_bids,
            "sum_asks": sum_asks,
            "ts": ts / 1000  # convert to detik
        })

    def analyze(self):
        results = []
        now = time.time()

        # Ambil semua sum_bids terakhir
        latest_bids = {
            symbol: dq[-1]["sum_bids"] if dq else 0
            for symbol, dq in self.data.items()
        }
        top5_bids = sorted(latest_bids.items(), key=lambda x: x[1], reverse=True)[:5]
        top5_symbols = {s for s, _ in top5_bids}

        for symbol, dq in self.data.items():
            item = {
                "symbol": symbol,
                "status": "ok",
                "score": 0,
                "ratio_now": None,
                "stabil": False,
                "dominasi_top5": False,
                "anti_spoof": False,
                "reason": []
            }

            if len(dq) < MAXLEN:
                item["status"] = "gugur"
                item["reason"].append("Data < 5 detik")
                results.append(item)
                continue

            ratios = [x["ratio"] for x in dq]
            ts_diff = now - dq[0]["ts"]
            item["ratio_now"] = ratios[-1]

            # Rule 1: Rasio harus di atas 1.6 semua
            if any(r < RATIO_THRESHOLD for r in ratios):
                item["status"] = "gugur"
                item["reason"].append("Rasio < 1.6 dalam 5 detik")
            else:
                item["stabil"] = True
                item["score"] += 1

            # Rule 2: Harus stabil selama 5 detik (selisih timestamp)
            if ts_diff < 5:
                item["status"] = "gugur"
                item["reason"].append("Durasi < 5 detik")

            # Rule 3: Dominasi TOP 5 berdasarkan sum_bids
            if symbol in top5_symbols:
                item["dominasi_top5"] = True
                item["score"] += 1
            else:
                item["reason"].append("Tidak dominan di TOP 5")

            # Rule 4: Anti spoofing - tidak boleh lonjakan mendadak
            diffs = [abs(ratios[i+1] - ratios[i]) for i in range(len(ratios)-1)]
            if all(diff <= 0.5 for diff in diffs):
                item["anti_spoof"] = True
                item["score"] += 1
            else:
                item["reason"].append("Rasio naik-turun mendadak")

            # Final: Set status gugur kalau salah satu komponen gagal
            if not (item["stabil"] and item["dominasi_top5"] and item["anti_spoof"]):
                item["status"] = "gugur"

            results.append(item)

        return results
