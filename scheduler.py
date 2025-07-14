import asyncio
from ws.binance_client import run_binance_ws, tracker
from globals import last_result

async def periodic_analysis():
    while True:
        last_result.clear()
        hasil = tracker.get_top_buy_ratio()
        print("Hasil analisa:", hasil)
        last_result.extend(hasil)
        await asyncio.sleep(5)

async def main():
    await asyncio.gather(
        run_binance_ws(),
        periodic_analysis()
    )

if __name__ == "__main__":
    asyncio.run(main())
