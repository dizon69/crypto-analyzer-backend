# backend/app/api/buyqueue.py

from fastapi import APIRouter, Depends
from app.collector.ws_collector import OrderbookCollector
from app.core.buyqueue_logic import BuyQueueAnalyzer

router = APIRouter()

# DI: collector instance (should be singleton/global, diinject dari main.py)
def get_collector():
    from app.main import collector  # global var collector di main.py
    return collector

@router.get("/buyqueue", tags=["BuyQueue"])
async def get_buyqueue(collector: OrderbookCollector = Depends(get_collector)):
    """
    Endpoint: /api/buyqueue
    Return hasil analisa buy queue semua coin, real-time
    """
    buffer = collector.get_all()        # snapshot buffer RAM dari collector
    analyzer = BuyQueueAnalyzer(buffer) # logic scoring
    result = analyzer.analyze_all()     # list hasil untuk semua coin
    return {"data": result}
