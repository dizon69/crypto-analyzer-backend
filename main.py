from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.buyqueue import router as buyqueue_router
from ws.binance_client import run_binance_ws
import asyncio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ganti sesuai kebutuhan
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(buyqueue_router, prefix="/api", tags=["BuyQueue"])

@app.on_event("startup")
async def start_ws():
    asyncio.create_task(run_binance_ws())
