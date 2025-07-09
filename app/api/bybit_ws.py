from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
import websockets
import json

router = APIRouter()

BYBIT_WS_URL = "wss://stream.bybit.com/v5/public/spot"

@router.websocket("/bybit")
async def bybit_ws_proxy(websocket: WebSocket):
    await websocket.accept()
    try:
        async with websockets.connect(BYBIT_WS_URL) as bybit_ws:
            subscribe_msg = {
                "op": "subscribe",
                "args": ["orderbook.1.BTCUSDT"]
            }
            await bybit_ws.send(json.dumps(subscribe_msg))
            while True:
                msg = await bybit_ws.recv()
                await websocket.send_text(msg)
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print("Error:", e)
        await websocket.close()
