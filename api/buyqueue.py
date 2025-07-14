### api/buyqueue.py
from fastapi import APIRouter
from globals import last_result

router = APIRouter()

@router.get("/buyqueue")
def get_buyqueue():
    return last_result