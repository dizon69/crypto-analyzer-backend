### ✅ 3. Lokasi: `app/scheduler/job_runner.py`

import asyncio
from app.services.binance_ws import start_binance_ws

async def run_jobs():
    asyncio.create_task(start_binance_ws())
