from fastapi import APIRouter
from logic.buyqueue import tracker

router = APIRouter()

@router.get("/buyqueue")
def get_buyqueue():
    return tracker.get_top_buy_ratio()
