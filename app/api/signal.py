from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_signal():
    return {"status": "ok", "data": "Dummy Signal"}
