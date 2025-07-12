# backend/app/core/binance_ws.py

import asyncio
import websockets
import json
import logging
from typing import List, Callable, Dict, Any

BINANCE_WS_BASE = "wss://stream.binance.com:9443/stream"
PING_INTERVAL = 170  # 170 detik (aman, di bawah 3 menit)
RECONNECT_DELAY = 5  # detik

class BinanceWSClient:
    def __init__(
        self,
        streams: List[str],
        on_message: Callable[[Dict[str, Any]], None],
        logger: logging.Logger = None
    ):
        """
        streams: List nama stream, contoh ["btcusdt@depth5@100ms", "btcusdt@kline_1h"]
        on_message: Fungsi callback untuk handle data masuk (async/sync)
        """
        self.streams = streams
        self.on_message = on_message
        self.ws = None
        self.running = False
        self.logger = logger or logging.getLogger("binance_ws")

    def _build_url(self):
        stream_str = '/'.join(self.streams)
        return f"{BINANCE_WS_BASE}?streams={stream_str}"

    async def _ping(self):
        try:
            if self.ws:
                await self.ws.ping()
                self.logger.debug("Ping sent to Binance WS")
        except Exception as e:
            self.logger.warning(f"Ping error: {e}")

    async def _keep_alive(self):
        while self.running:
            await asyncio.sleep(PING_INTERVAL)
            await self._ping()

    async def run(self):
        url = self._build_url()
        self.running = True
        while self.running:
            try:
                self.logger.info(f"Connecting to Binance WS: {url}")
                async with websockets.connect(url, ping_interval=None) as ws:
                    self.ws = ws
                    ping_task = asyncio.create_task(self._keep_alive())
                    async for msg in ws:
                        try:
                            data = json.loads(msg)
                            # Bisa handle sync/async callback
                            res = self.on_message(data)
                            if asyncio.iscoroutine(res):
                                await res
                        except Exception as e:
                            self.logger.error(f"Parse error: {e}")
                    ping_task.cancel()
            except Exception as e:
                self.logger.warning(f"WS error: {e}, reconnecting in {RECONNECT_DELAY}s...")
                await asyncio.sleep(RECONNECT_DELAY)

    def stop(self):
        self.running = False

# ====== Example manual run (not production, buat debug aja) ======
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    streams = [
        "btcusdt@depth5@100ms",
        "btcusdt@kline_1m",
        "ethusdt@depth5@100ms",
        "ethusdt@kline_1m"
    ]

    def print_msg(data):
        print(json.dumps(data, indent=2))

    ws_client = BinanceWSClient(streams, print_msg)
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(ws_client.run())
    except KeyboardInterrupt:
        ws_client.stop()
