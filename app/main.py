from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import bybit_ws, coingecko, buyqueue
import asyncio
from app.collector.websocket_collector import start_binance_listener

app = FastAPI()

# ✅ Tambahkan whitelist domain frontend kamu
origins = [
    "https://crypto-analyzer.vercel.app",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Include router
app.include_router(bybit_ws.router, prefix="/api/v1/ws", tags=["WebSocket"])
app.include_router(coingecko.router, prefix="/api/v1/coingecko", tags=["CoinGecko"])
app.include_router(buyqueue.router, prefix="/api", tags=["BuyQueue"])

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(start_binance_listener())
