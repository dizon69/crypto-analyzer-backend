from fastapi import APIRouter
import httpx, time

router = APIRouter()
cache = {"data": None, "timestamp": 0}
CACHE_DURATION = 30  # detik

@router.get("/top-gainer-loser")
async def top_gainer_loser():
    if time.time() - cache["timestamp"] < CACHE_DURATION:
        return cache["data"]

    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 100,
        "page": 1,
    }
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=params)
        data = resp.json()

    sorted_data = sorted(data, key=lambda x: x.get("price_change_percentage_24h", 0) or 0)
    top_gainers = sorted_data[-10:][::-1]
    top_losers = sorted_data[:10]

    result = {"gainers": top_gainers, "losers": top_losers}
    cache["data"] = result
    cache["timestamp"] = time.time()
    return result
