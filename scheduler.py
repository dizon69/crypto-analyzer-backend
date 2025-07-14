### scheduler.py
import asyncio
from ws.binance_client import run_binance_ws, tracker
from globals import last_result
from logic.buyqueue import BuySellRatioTracker

async def periodic_analysis():
    while True:
        last_result.clear()
        last_result.extend(tracker.get_top_buy_ratio())
        await asyncio.sleep(5)

async def main():
    await asyncio.gather(
        run_binance_ws(),
        periodic_analysis()
    )

if __name__ == "__main__":
    asyncio.run(main())