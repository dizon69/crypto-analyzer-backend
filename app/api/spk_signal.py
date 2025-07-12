# backend/app/api/spk_signal.py

from fastapi import APIRouter, Depends
from app.core.spk_signal import SPKSignal
from app.api.buyqueue import get_collector as get_buyqueue_collector
from app.api.volume import get_kline_collector as get_volume_collector
from app.api.breakout import get_kline_collector as get_breakout_collector
from app.api.ema import get_kline_collector as get_ema_collector
from app.api.rsi import get_kline_collector as get_rsi_collector

from app.core.buyqueue_logic import BuyQueueAnalyzer
from app.core.volume_logic import VolumeAnalyzer
from app.core.breakout_logic import BreakoutAnalyzer, default_resistance
from app.core.ema_logic import EMAAnalyzer
from app.core.rsi_logic import RSIAnalyzer

router = APIRouter()

@router.get("/spk-signal", tags=["SPKSignal"])
async def get_spk_signal(
    buyqueue_collector = Depends(get_buyqueue_collector),
    volume_collector = Depends(get_volume_collector),
    breakout_collector = Depends(get_breakout_collector),
    ema_collector = Depends(get_ema_collector),
    rsi_collector = Depends(get_rsi_collector),
):
    # Jalankan analisa untuk semua indikator
    buyqueue = BuyQueueAnalyzer(buyqueue_collector.get_all()).analyze_all()
    volume = VolumeAnalyzer(volume_collector.get_all()).analyze_all()
    breakout = BreakoutAnalyzer(breakout_collector.get_all(), default_resistance).analyze_all()
    ema = EMAAnalyzer(ema_collector.get_all()).analyze_all()
    rsi = RSIAnalyzer(rsi_collector.get_all()).analyze_all()

    # Gabungkan hasil semua logic ke SPK signal
    spk = SPKSignal(
        buyqueue,
        volume,
        breakout,
        ema,
        rsi
    )
    result = spk.combine()
    return {"data": result}
