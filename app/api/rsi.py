# backend/app/api/rsi.py

from fastapi import APIRouter, Depends
from app.core.rsi_logic import RSIAnalyzer

router = APIRouter()

def get_kline_collector():
    from app.main import kline_collector
    return kline_collector

@router.get("/rsi", tags=["RSI"])
async def get_rsi(kline_collector = Depends(get_kline_collector)):
    buffer = kline_collector.get_all()
    analyzer = RSIAnalyzer(buffer)
    result = analyzer.analyze_all()
    return {"data": result}
