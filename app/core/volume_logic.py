# backend/app/core/volume_logic.py

from typing import List, Dict, Any

class VolumeAnalyzer:
    def __init__(self, kline_buffer: Dict[str, List[dict]]):
        """
        kline_buffer: {symbol: [ {close_time, close, volume}, ... ]}
        """
        self.buffer = kline_buffer

    def analyze_symbol(self, symbol: str) -> dict:
        dq: List[dict] = self.buffer.get(symbol, [])
        result = {
            "symbol": symbol,
            "status": "gugur",
            "volume_24h": None,
            "rvol": None,
            "price_now": None,
            "spike": False,
            "price_up": False,
            "reason": [],
            "score": 0,
        }
        if len(dq) < 4:  # butuh minimal 4 candle (3h sebelum + sekarang)
            result["reason"].append("Candle < 4 jam")
            return result

        # Ambil volume 24 jam terakhir (sum 24 candle, tapi pakai 6 jam dulu kalau sample sedikit)
        recent = dq[-3:]  # 3 jam terakhir, bisa adjust
        prev = dq[:-3]    # jam sebelumnya

        volume_24h = sum(c["volume"] for c in dq)
        price_now = recent[-1]["close"]
        price_before = prev[-1]["close"] if prev else price_now

        result["volume_24h"] = volume_24h
        result["price_now"] = price_now

        # --- 1. Volume 24 jam 100-800 juta USDT
        if not (100_000_000 <= volume_24h <= 800_000_000):
            result["reason"].append("Volume 24 jam tidak di range 100-800 juta")
        else:
            result["score"] += 8

        # --- 2. RVOL <= 1.6
        if len(dq) < 4:
            rvol = None
        else:
            avg_prev = sum(c["volume"] for c in dq[:-1]) / (len(dq) - 1)
            rvol = dq[-1]["volume"] / avg_prev if avg_prev > 0 else 0
        result["rvol"] = rvol

        if rvol is None or rvol > 1.6:
            result["reason"].append("RVOL > 1.6")
        else:
            result["score"] += 8

        # --- 3. Volume spike? (kalau volume besar hanya 1 candle, bukan naik bertahap)
        spike = (dq[-1]["volume"] > 2 * max(c["volume"] for c in dq[:-1]))
        result["spike"] = spike
        if spike:
            result["reason"].append("Volume spike (hanya 1 candle)")
        else:
            result["score"] += 4

        # --- 4. Harga naik (candle terakhir naik vs sebelumnya)
        price_up = price_now > price_before
        result["price_up"] = price_up
        if not price_up:
            result["reason"].append("Harga tidak naik bareng volume")
        else:
            result["score"] += 5

        # --- FINAL STATUS
        if result["score"] >= 20:  # threshold lolos (bisa adjust)
            result["status"] = "lolos"

        return result

    def analyze_all(self) -> List[dict]:
        return [self.analyze_symbol(sym) for sym in self.buffer.keys()]
