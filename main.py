from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.buyqueue import router as buyqueue_router

app = FastAPI()

# ⬇️ Tambahkan middleware CORS di sini
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://crypto-analyzer.com,"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(buyqueue_router, prefix="/api", tags=["BuyQueue"])
