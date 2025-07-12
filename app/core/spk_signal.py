# backend/app/core/spk_signal.py

from typing import Dict, List

class SPKSignal:
    def __init__(
        self,
        buyqueue_result: List[dict],
        volume_result: List[dict],
        breakout_result: List[dict],
        ema_result: List[dict],
        rsi_result: List[dict],
    ):
        self.buyqueue = {x["symbol"]: x for x in buyqueue_result}
        self.volume = {x["symbol"]: x for x in volume_result}
        self.breakout = {x["symbol"]: x for x in breakout_result}
        self.ema = {x["symbol"]: x for x in ema_result}
        self.rsi = {x["symbol"]: x for x in rsi_result}

    def combine(self) -> List[dict]:
        coins = set(self.buyqueue.keys())
        final = []
        for symbol in coins:
            score = 0
            status = "gugur"
            detail = {}

            bq = self.buyqueue.get(symbol, {})
            vol = self.volume.get(symbol, {})
            br = self.breakout.get(symbol, {})
            ema = self.ema.get(symbol, {})
            rsi = self.rsi.get(symbol, {})

            score += bq.get("score", 0)
            score += vol.get("score", 0)
            score += br.get("score", 0)
            score += ema.get("score", 0)
            score += rsi.get("score", 0)

            # Syarat: semua indikator tidak gugur
            if (
                bq.get("status") == "lolos" and
                vol.get("status") == "lolos" and
                br.get("status") == "lolos" and
                ema.get("status") == "lolos" and
                rsi.get("status") == "lolos"
            ):
                status = "aktif"
            else:
                status = "gugur"

            # Harga Buy: ambil dari breakout atau ema, fallback ke volume/price_now
            harga_buy = br.get("close_now") or ema.get("cross_price") or vol.get("price_now")
            target_sell = round(harga_buy * 1.02, 6) if harga_buy else None
            cutloss = round(harga_buy * 0.98, 6) if harga_buy else None

            detail = {
                "buyqueue": bq.get("score", 0),
                "volume": vol.get("score", 0),
                "breakout": br.get("score", 0),
                "ema": ema.get("score", 0),
                "rsi": rsi.get("score", 0),
            }

            final.append({
                "symbol": symbol,
                "score": score,
                "status": status,
                "harga_buy": harga_buy,
                "target_sell": target_sell,
                "cutloss": cutloss,
                "detail": detail,
            })

        # Urutkan berdasarkan score
        final = sorted(final, key=lambda x: x["score"], reverse=True)
        return final[:10]   # Top 10
