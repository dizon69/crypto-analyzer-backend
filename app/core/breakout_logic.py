# backend/app/core/breakout_logic.py

from typing import List, Dict

class BreakoutAnalyzer:
    def __init__(self, kline_buffer: Dict[str, List[dict]], resistance_dict: Dict[str, float]):
        """
        kline_buffer: {symbol: [ {close_time, close, volume}, ... ]}
        resistance_dict: {symbol: resistance_price}
        """
        self.buffer = kline_buffer
        self.resistance = resistance_dict

    def analyze_symbol(self, symbol: str) -> dict:
        dq = self.buffer.get(symbol, [])
        resistance = self.resistance.get(symbol)
        result = {
            "symbol": symbol,
            "status": "gugur",
            "close_now": None,
            "resistance": resistance,
            "body_pct": None,
            "vol_vs_avg": None,
            "break_valid": False,
            "hold": False,
            "reason": [],
            "score": 0,
        }
        if not resistance or len(dq) < 4:
            result["reason"].append("Belum ada resistance / data kline < 4")
            return result

        # --- Ambil candle terakhir (close sudah di atas resistance?) ---
        c = dq[-1]
        prev3 = dq[-4:-1]  # 3 candle sebelum
        close_now = c["close"]
        result["close_now"] = close_now

        if close_now <= resistance:
            result["reason"].append("Belum break resistance")
            return result

        # --- 1. Close candle harus di atas resistance ---
        result["break_valid"] = True

        # --- 2. Body candle harus 60-70% total panjang candle ---
        # Simulasi data: aslinya harus dapat open/high/low/close, volume
        # Di contoh ini hanya pakai close (jika mau, bisa tambah parse open/high/low)
        # (asumsi: body% = abs(close-open)/(high-low))
        # Untuk real, wajib pake data full OHLCV di collector!
        # Sementara, auto lolos (nanti tinggal tambahkan logic ini)
        result["body_pct"] = 0.7  # placeholder

        # --- 3. Volume candle harus > rata-rata 3 sebelumnya ---
        vol_now = c["volume"]
        vol_avg = sum(x["volume"] for x in prev3) / 3 if prev3 else 0
        result["vol_vs_avg"] = (vol_now / vol_avg) if vol_avg > 0 else None

        if vol_avg == 0 or vol_now < vol_avg:
            result["reason"].append("Volume break < rata-rata 3 sebelumnya")
        else:
            result["score"] += 7

        # --- 4. Setelah break, harga harus bertahan (tidak langsung turun) ---
        # Syarat: close candle berikutnya masih di atas resistance (jika ada)
        hold = len(dq) >= 2 and dq[-1]["close"] > resistance and dq[-2]["close"] > resistance
        result["hold"] = hold
        if not hold:
            result["reason"].append("Harga tidak bertahan di atas resistance")
        else:
            result["score"] += 8

        # --- 5. Valid breakout: break + volume + body% lolos + hold ---
        if result["break_valid"] and result["vol_vs_avg"] and result["vol_vs_avg"] > 1.0 and hold:
            result["status"] = "lolos"
            result["score"] += 7
        else:
            result["status"] = "gugur"

        return result

    def analyze_all(self) -> List[dict]:
        return [self.analyze_symbol(sym) for sym in self.buffer.keys()]

        # =======================
# Default Resistance Dict
# =======================

# Isi manual atau biarin kosong dulu, nanti bisa diupdate otomatis
default_resistance = {
    "BTCUSDT": 69000,
    "ETHUSDT": 3500,
    "BNBUSDT": 600,
    "SOLUSDT": 150,
    "ADAUSDT": 0.5,
    "XRPUSDT": 0.8,
    "DOGEUSDT": 0.15,
    "MATICUSDT": 1.2,
    "LTCUSDT": 90,
    "LINKUSDT": 15
}

