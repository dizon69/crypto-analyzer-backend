# backend/app/core/ema_logic.py

from typing import List, Dict

def calc_ema(prices: List[float], period: int) -> List[float]:
    """Calculate EMA (Exponential Moving Average) list."""
    emas = []
    k = 2 / (period + 1)
    for i, price in enumerate(prices):
        if i < period - 1:
            emas.append(None)
        elif i == period - 1:
            emas.append(sum(prices[:period]) / period)
        else:
            emas.append(price * k + emas[-1] * (1 - k))
    return emas

class EMAAnalyzer:
    def __init__(self, kline_buffer: Dict[str, List[dict]]):
        """
        kline_buffer: {symbol: [ {close_time, close, volume}, ... ]}
        """
        self.buffer = kline_buffer

    def analyze_symbol(self, symbol: str) -> dict:
        dq = self.buffer.get(symbol, [])
        result = {
            "symbol": symbol,
            "status": "gugur",
            "cross": False,
            "cross_price": None,
            "vol_cross": None,
            "valid_cross": False,
            "ema5_above_ema20": 0,
            "reason": [],
            "score": 0,
        }
        if len(dq) < 25:
            result["reason"].append("Kline < 25 candle (butuh 20+ untuk EMA20)")
            return result

        closes = [c["close"] for c in dq]
        vols = [c["volume"] for c in dq]

        ema5 = calc_ema(closes, 5)
        ema20 = calc_ema(closes, 20)

        # Cari cross up (EMA5 dari bawah ke atas EMA20)
        cross_idx = None
        for i in range(20, len(closes)):
            if ema5[i-1] is not None and ema20[i-1] is not None:
                if ema5[i-1] < ema20[i-1] and ema5[i] > ema20[i]:
                    cross_idx = i
        if cross_idx is None:
            result["reason"].append("Belum ada cross up EMA5>EMA20")
            return result

        result["cross"] = True
        result["cross_price"] = closes[cross_idx]
        result["vol_cross"] = vols[cross_idx]

        # Validasi cross: volume naik dibanding rata2 3 candle sebelumnya
        if cross_idx >= 3:
            vol_avg = sum(vols[cross_idx-3:cross_idx]) / 3
            if vols[cross_idx] > vol_avg:
                result["valid_cross"] = True
                result["score"] += 7
            else:
                result["reason"].append("Volume cross tidak naik")
        else:
            result["reason"].append("Data volume sebelum cross kurang")

        # EMA5 tetap di atas EMA20 selama minimal 2 candle setelah cross
        stay_above = 0
        for j in range(cross_idx+1, min(len(closes), cross_idx+4)):
            if ema5[j] > ema20[j]:
                stay_above += 1
        result["ema5_above_ema20"] = stay_above
        if stay_above >= 2:
            result["score"] += 8
        else:
            result["reason"].append("EMA5 tidak bertahan di atas EMA20 2 candle setelah cross")

        # Status lolos kalau valid cross dan EMA5 di atas EMA20 >=2 candle
        if result["valid_cross"] and stay_above >= 2:
            result["status"] = "lolos"
            result["score"] += 7

        return result

    def analyze_all(self) -> List[dict]:
        return [self.analyze_symbol(sym) for sym in self.buffer.keys()]
