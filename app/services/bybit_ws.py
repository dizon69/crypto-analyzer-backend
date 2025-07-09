import asyncio
import websockets

BYBIT_WS_URL = "wss://stream.bybit.com/v5/public/spot"

async def test_bybit_ws(symbol="BTCUSDT"):
    stream = f"{symbol.lower()}@depth"
    ws_url = f"{BYBIT_WS_URL}?stream={stream}"
    print(f"Connecting to: {ws_url}")

    async with websockets.connect(ws_url) as websocket:
        while True:
            msg = await websocket.recv()
            print(f"[BYBIT WS] {msg}")
