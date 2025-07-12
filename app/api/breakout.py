# backend/app/api/breakout.py

from fastapi import APIRouter, Depends
from app.core.breakout_logic import BreakoutAnalyzer

router = APIRouter()

def get_kline_collector():
    from app.main import kline_collector
    return kline_collector

# --- Simulasi resistance, bisa update nanti pake logic/AI/manual dsb
default_resistance = {
    "btcusdt": 60000,
    "ethusdt": 3500,
    "bnbusdt": 600,
    "solusdt": 170,
    "adausdt": 0.5,
    "xrpusdt": 0.65,
    "dogeusdt": 0.2,
    "maticusdt": 0.7,
    "ltcusdt": 90,
    "linkusdt": 16,
}

@router.get("/breakout", tags=["Breakout"])
async def get_breakout(kline_collector = Depends(get_kline_collector)):
    buffer = kline_collector.get_all()
    analyzer = BreakoutAnalyzer(buffer, default_resistance)
    result = analyzer.analyze_all()
    return {"data": result}
