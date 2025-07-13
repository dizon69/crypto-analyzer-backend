from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from collector.binance_ws import get_top_buy_data, collect_data
import asyncio

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.on_event("startup")
async def startup_event():
    loop = asyncio.get_event_loop()
    loop.create_task(collect_data())

@app.get("/api/top-buy-queue")
def top_buy():
    return get_top_buy_data()
