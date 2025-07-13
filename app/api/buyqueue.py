from fastapi import APIRouter
from app.core.globals import tracker
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/buyqueue")
def get_buyqueue_raw():
    return JSONResponse(content=tracker.get_latest())
