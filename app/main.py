from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import buyqueue
from app.scheduler.job_runner import run_jobs
from app.collector.buyqueue_collector import collect
import asyncio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://crypto-analyzer.com",
                   "https://www.crypto-analyzer.com",
                   "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(run_jobs())
    asyncio.create_task(collect())  # ⬅️ Ini yang ngejalanin WebSocket

app.include_router(buyqueue.router, prefix="/api")
