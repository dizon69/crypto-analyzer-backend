from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.buyqueue import router as buyqueue_router

app = FastAPI()

# Middleware CORS WAJIB TARO DI BAWAH app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://crypto-analyzer.com",
        "https://www.crypto-analyzer.com",
        "https://crypto-analyzer-frontend.vercel.app",
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register router API lo (ganti kalau router lo beda)
app.include_router(buyqueue_router, prefix="/api", tags=["BuyQueue"])
