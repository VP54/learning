import asyncio
from typing import Iterable, Optional
import json
import time
from concurrent.futures import ThreadPoolExecutor
from websocket import WebSocketApp
from polymarket_dashboard.src.config.logger import logger
from polymarket_dashboard.src.config.enum import Exchange


class WebSocketListener:

    def __init__(self, url, asset_ids, queue, loop, market_channel, logger=logger):
        self.url = url
        self.asset_ids = set(asset_ids)
        self.queue = queue
        self.loop = loop
        self.market_channel = market_channel
        self.logger = logger

        self.executor = ThreadPoolExecutor(
            max_workers=1,
            thread_name_prefix="WS-Reconnect"
        )
        self._reconnecting = False
        self._create_ws()
        self._lock = asyncio.Lock()

    def _create_ws(self):
        self.ws = WebSocketApp(
            f"{self.url}/ws/{self.market_channel}",
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
        )

    async def add_asset_ids(self, asset_ids: Iterable[str]):
        """
        Incrementally subscribe to NEW asset_ids only.
        Safe to call periodically.
        Non-blocking.
        """

        incoming = set(asset_ids)

        # fast path — no await
        new_ids = incoming - self.asset_ids
        if not new_ids:
            return

        loop = asyncio.get_running_loop()

        async with self._lock:
            # re-check under lock
            new_ids = incoming - self.asset_ids
            if not new_ids:
                return

            # update state first (important)
            self.asset_ids |= new_ids

            for asset_id in new_ids:
                msg = {
                    "type": "subscribe",
                    "channel": self.market_channel,
                    "asset_id": asset_id,
                }

                loop.call_soon_threadsafe(
                    self.ws.send,
                    json.dumps(msg),
                )

    def on_open(self, ws):
        try:
            ws.send(
                json.dumps(
                    {"type": self.market_channel, "assets_ids": list(self.asset_ids)}
                )
            )
            ws.send(
                json.dumps(
                    {"operation": "subscribe", "assets_ids": list(self.asset_ids)}
                )
            )
            logger.info("WebSocket subscribed")
        except Exception:
            logger.exception("Failed during on_open")

    def on_message(self, ws, message):
        if not message or message == "NO NEW ASSETS":
            return

        try:
            msg = json.loads(message)
        except json.JSONDecodeError:
            logger.warning("Bad JSON: %r", message)
            return

        if isinstance(msg, list):
            for event in msg:
                self._handle_event(event)
        elif isinstance(msg, dict):
            self._handle_event(msg)

    def _handle_event(self, event):
        if event.get("event_type") == "book":
            self.loop.call_soon_threadsafe(
                self.queue.put_nowait,
                (Exchange.Polymarket.value, event)
            )

    def on_error(self, ws, error):
        logger.warning("[WS] error: %s", error)
        self._schedule_reconnect()

    def on_close(self, ws, code, msg):
        logger.info("[WS] closed: %s %s", code, msg)

    def _schedule_reconnect(self):
        if self._reconnecting:
            return
        self._reconnecting = True
        self.executor.submit(self._reconnect)

    def _reconnect(self):
        time.sleep(1)
        logger.info("Reconnecting websocket...")
        self._create_ws()
        self._reconnecting = False
        self.run()

    def run(self):
        self.ws.run_forever(
            ping_interval=10,
            ping_timeout=5
        )
