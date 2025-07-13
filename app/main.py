### ✅ 5. Lokasi: `app/main.py`

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import buyqueue
from app.scheduler.job_runner import run_jobs
import asyncio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(run_jobs())

app.include_router(buyqueue.router, prefix="/api")