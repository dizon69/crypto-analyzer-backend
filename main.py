### main.py
from fastapi import FastAPI
from api.buyqueue import router as buyqueue_router

app = FastAPI()

app.include_router(buyqueue_router, prefix="/api", tags=["BuyQueue"])
