from fastapi import APIRouter
from app.services.binance_ws import get_top_buyqueue
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/buyqueue")
def get_buyqueue():
    data = get_top_buyqueue()
    return JSONResponse(content=data)