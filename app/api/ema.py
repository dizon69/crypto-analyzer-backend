# backend/app/api/ema.py

from fastapi import APIRouter, Depends
from app.core.ema_logic import EMAAnalyzer

router = APIRouter()

def get_kline_collector():
    from app.main import kline_collector
    return kline_collector

@router.get("/ema", tags=["EMA"])
async def get_ema(kline_collector = Depends(get_kline_collector)):
    buffer = kline_collector.get_all()
    analyzer = EMAAnalyzer(buffer)
    result = analyzer.analyze_all()
    return {"data": result}
