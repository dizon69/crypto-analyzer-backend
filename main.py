from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.buyqueue import router as buyqueue_router
import asyncio
from ws.binance_client import run_binance_ws

app = FastAPI()

# --- CORS Setting kamu, GAK DIUBAH ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://crypto-analyzer.com",
        "https://www.crypto-analyzer.com",
        "https://crypto-analyzer-frontend.vercel.app",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(buyqueue_router, prefix="/api", tags=["BuyQueue"])

# Collector jalan di startup
@app.on_event("startup")
async def start_collector():
    loop = asyncio.get_event_loop()
    loop.create_task(run_binance_ws())
