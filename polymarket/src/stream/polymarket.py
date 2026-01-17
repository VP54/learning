import os
import json
from queue import Queue
from websocket import WebSocketApp
from dotenv import load_dotenv



class WebSocketListener:
    """Simple websocket listener fo Polymarket.

    Example:
        listener = WebSocketListener(url, asset_ids, queue=queue, loop=loop, market_channel=MARKET_CHANNEL)
        loop.run_in_executor(executor, listener.run),
    """
    def __init__(self, url, asset_ids, queue, loop, market_channel):
        self.url = url
        self.asset_ids = asset_ids
        self.queue = queue
        self.loop = loop
        self.market_channel = market_channel

        self.ws = WebSocketApp(
            f"{url}/ws/{market_channel}",
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
        )

    def on_open(self, ws):
        ws.send(json.dumps({
            "type": self.market_channel,
            "assets_ids": self.asset_ids
        }))
        ws.send(json.dumps({
            "operation": "subscribe",
            "assets_ids": self.asset_ids
        }))

    def on_message(self, ws, message):
        if message == "NO NEW ASSETS":
            return
        # thread → asyncio safely
        self.loop.call_soon_threadsafe(self.queue.put_nowait, ("POLYMARKET", message))

    def on_error(self, ws, error):
        print("[WS] Error:", error)

    def on_close(self, ws, code, msg):
        print("[WS] Closed:", code, msg)

    def run(self):
        self.ws.run_forever(ping_interval=None)
