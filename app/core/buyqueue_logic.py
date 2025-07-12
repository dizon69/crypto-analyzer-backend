# backend/app/core/buyqueue_logic.py

from collections import deque
from typing import List, Dict, Any

class BuyQueueAnalyzer:
    def __init__(self, buffer: Dict[str, List[dict]]):
        """
        buffer: dict hasil dari collector, {symbol: [ {ratio, sum_bids, sum_asks, ts}, ... ]}
        """
        self.buffer = buffer

    def analyze_symbol(self, symbol: str) -> dict:
        """
        Analisa 5 detik terakhir 1 coin. 
        Return: dict detail hasil penilaian buy queue sesuai logic file lo
        """
        dq: List[dict] = self.buffer.get(symbol, [])
        result = {
            "symbol": symbol,
            "status": "gugur",
            "ratio_now": None,
            "stabil": False,
            "dominasi_top5": False,
            "anti_spoof": False,
            "reason": [],
            "score": 0,
        }
        if len(dq) < 5:
            result["reason"].append("Data < 5 detik")
            return result

        ratios = [item["ratio"] for item in dq]
        sum_bids = [item["sum_bids"] for item in dq]
        sum_asks = [item["sum_asks"] for item in dq]

        # --- 1. Rasio > 1.6 setiap detik, minimal 5 detik berturut
        threshold = 1.6
        stabil = all(r > threshold for r in ratios)
        result["stabil"] = stabil
        result["ratio_now"] = ratios[-1]
        if not stabil:
            result["reason"].append("Rasio buy/sell < 1.6 dalam 5 detik")
        
        # --- 2. Anti spike: rasio gak boleh naik turun tajam (bukan spoof)
        # Definisi: selisih tertinggi-terendah rasio dalam 5 detik tidak ekstrim
        max_r, min_r = max(ratios), min(ratios)
        anti_spoof = (max_r - min_r) < 1.0  # max 1x fluktuasi, bisa adjust
        result["anti_spoof"] = anti_spoof
        if not anti_spoof:
            result["reason"].append("Fluktuasi/spike ratio terlalu tinggi (spoofing?)")

        # --- 3. Dominasi Top 5 (jumlah bid top 5 jauh di atas ask top 5)
        # Syarat: sum_bids > sum_asks di semua detik
        dominasi = all(b > a for b, a in zip(sum_bids, sum_asks))
        result["dominasi_top5"] = dominasi
        if not dominasi:
            result["reason"].append("Tidak dominan di top 5 orderbook (bids <= asks)")
        
        # --- FINAL STATUS
        if stabil and anti_spoof and dominasi:
            result["status"] = "lolos"
            result["score"] = 25   # full point SPK
        else:
            result["status"] = "gugur"
            result["score"] = 0

        return result

    def analyze_all(self) -> List[dict]:
        """
        Kembalikan hasil penilaian semua coin.
        """
        return [self.analyze_symbol(sym) for sym in self.buffer.keys()]

# ========== USAGE (for API/backend) ==========
if __name__ == "__main__":
    # Simulasi data dummy dari collector
    dummy_buffer = {
        "btcusdt": [
            {"ratio": 1.72, "sum_bids": 8000, "sum_asks": 4000, "ts": 1},
            {"ratio": 1.81, "sum_bids": 8200, "sum_asks": 4100, "ts": 2},
            {"ratio": 1.68, "sum_bids": 7900, "sum_asks": 4300, "ts": 3},
            {"ratio": 1.77, "sum_bids": 8300, "sum_asks": 4200, "ts": 4},
            {"ratio": 1.82, "sum_bids": 8500, "sum_asks": 4200, "ts": 5},
        ]
    }
    analyzer = BuyQueueAnalyzer(dummy_buffer)
    print(analyzer.analyze_all())
