# backend/app/api/buyqueue.py

from fastapi import APIRouter
from app.core import globals

router = APIRouter()

@router.get("/buyqueue")
async def get_buyqueue():
    if not globals.buyqueue_analyzer:
        return {"error": "Analyzer belum siap"}

    try:
        results = globals.buyqueue_analyzer.analyze()
        return {"data": results}
    except Exception as e:
        return {"error": str(e)}
