from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import buyqueue
from app.collector.ws_collector import start_collector
from app.api import breakout         # <--- tambahkan di sini
from app.api import ema 
from app.api import volume
from app.api import rsi
from app.api import spk_signal
import asyncio

SYMBOLS = [
    "btcusdt", "ethusdt", "bnbusdt", "solusdt", "adausdt",
    "xrpusdt", "dogeusdt", "maticusdt", "ltcusdt", "linkusdt"
]

app = FastAPI()

# --- CORS whitelist frontend lo ---
origins = [
    "https://crypto-analyzer.vercel.app",
    "http://localhost:5173",
    "http://localhost:3000"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ====== GLOBAL COLLECTORS ======
collector = None
kline_collector = None

@app.on_event("startup")
async def startup_event():
    global collector, kline_collector
    collector, kline_collector = await start_collector(SYMBOLS)

app.include_router(buyqueue.router, prefix="/api")
app.include_router(volume.router, prefix="/api")
app.include_router(breakout.router, prefix="/api")
app.include_router(ema.router, prefix="/api")
app.include_router(rsi.router, prefix="/api")
app.include_router(spk_signal.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Crypto Analyzer Backend Running!"}
