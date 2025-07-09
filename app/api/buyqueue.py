from fastapi import APIRouter
from app.core.buyqueue_logic import get_top_buyqueue

router = APIRouter()

@router.get("/buyqueue")
def buyqueue_top10():
    return get_top_buyqueue()
