from fastapi import APIRouter
from app.services.binance_ws import get_top_buyqueue

router = APIRouter()

@router.get("/buyqueue")
def get_buyqueue():
    return get_top_buyqueue()