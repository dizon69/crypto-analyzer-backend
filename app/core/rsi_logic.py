# backend/app/core/rsi_logic.py

from typing import List, Dict

def calc_rsi(prices: List[float], period: int = 14) -> List[float]:
    rsi = []
    deltas = [prices[i] - prices[i-1] for i in range(1, len(prices))]
    gain = [max(d, 0) for d in deltas]
    loss = [abs(min(d, 0)) for d in deltas]
    avg_gain = sum(gain[:period]) / period if len(gain) >= period else 0
    avg_loss = sum(loss[:period]) / period if len(loss) >= period else 0
    if avg_loss == 0:
        rsi = [100] * len(prices)
    else:
        rsi = [None] * period  # first N is not valid
        rsi.append(100 - 100 / (1 + avg_gain / avg_loss))
        for i in range(period, len(gain)):
            avg_gain = (avg_gain * (period - 1) + gain[i]) / period
            avg_loss = (avg_loss * (period - 1) + loss[i]) / period
            if avg_loss == 0:
                rsi.append(100)
            else:
                rsi.append(100 - 100 / (1 + avg_gain / avg_loss))
    return rsi

class RSIAnalyzer:
    def __init__(self, kline_buffer: Dict[str, List[dict]]):
        self.buffer = kline_buffer

    def analyze_symbol(self, symbol: str) -> dict:
        dq = self.buffer.get(symbol, [])
        result = {
            "symbol": symbol,
            "status": "gugur",
            "rsi_now": None,
            "score": 0,
            "reason": [],
        }
        if len(dq) < 15:
            result["reason"].append("Kline < 15, tidak cukup untuk RSI")
            return result

        closes = [c["close"] for c in dq]
        rsi_series = calc_rsi(closes)
        rsi_now = rsi_series[-1] if rsi_series[-1] is not None else rsi_series[-2]
        result["rsi_now"] = rsi_now

        if rsi_now < 60:
            result["status"] = "lolos"
            result["score"] = 15
        else:
            result["reason"].append("RSI >= 60")

        return result

    def analyze_all(self) -> List[dict]:
        return [self.analyze_symbol(sym) for sym in self.buffer.keys()]
