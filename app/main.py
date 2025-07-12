# backend/app/main.py

from fastapi import FastAPI
from app.api import buyqueue
from app.core import globals
from app.analyzer.buyqueue_logic import BuyQueueAnalyzer
from app.config import SYMBOLS

app = FastAPI()

# ✅ Router
app.include_router(buyqueue.router, prefix="/api", tags=["BuyQueue"])

@app.on_event("startup")
async def startup_event():
    from app.collector.websocket_collector import start_collector
    import asyncio

    orderbook_collector, _ = await start_collector(SYMBOLS)
    globals.orderbook_collector = orderbook_collector

    # Inisialisasi dan simpan analyzer
    analyzer = BuyQueueAnalyzer(SYMBOLS)
    globals.buyqueue_analyzer = analyzer

    # ✅ Loop analisa tiap detik
    async def update_loop():
        while True:
            for sym in SYMBOLS:
                dq = orderbook_collector.get_last_n(sym, 1)
                if dq:
                    latest = dq[-1]
                    analyzer.update(
                        sym,
                        latest["ratio"],
                        latest["sum_bids"],
                        latest["sum_asks"],
                        latest["ts"]  # sudah dalam ms
                    )
            await asyncio.sleep(1)

    asyncio.create_task(update_loop())
