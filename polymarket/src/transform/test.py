import websocket
import json
import threading
from queue import Queue



from websocket import WebSocketApp
import json
import time
import threading

MARKET_CHANNEL = "market"
USER_CHANNEL = "user"


import json
import threading
import time
import websocket
from websocket import WebSocketApp

MARKET_CHANNEL = "market"
USER_CHANNEL = "user"


import json
import threading
import time
import websocket
from websocket import WebSocketApp

MARKET_CHANNEL = "market"


import json
import threading
import time
import websocket
from queue import Queue
from websocket import WebSocketApp

MARKET_CHANNEL = "market"


class WebSocketListener:
    def __init__(self, url, asset_ids, queue: Queue):
        self.url = url
        self.asset_ids = asset_ids
        self.queue = queue

        self.ws = WebSocketApp(
            f"{url}/ws/{MARKET_CHANNEL}",
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
        )

    def on_open(self, ws):
        ws.send(json.dumps({
            "type": MARKET_CHANNEL,
            "assets_ids": self.asset_ids
        }))
        ws.send(json.dumps({
            "operation": "subscribe",
            "assets_ids": self.asset_ids
        }))

    def on_message(self, ws, message):
        if message == "NO NEW ASSETS":
            return
        print(message)
        self.queue.put(message)  # O(1), non-blocking

    def on_error(self, ws, error):
        print("[WS] Error:", error)

    def on_close(self, ws, code, msg):
        print("[WS] Closed:", code, msg)

    def run(self):
        self.ws.run_forever(ping_interval=None)



MARKET_CHANNEL = "market"
USER_CHANNEL = "user"
import os


from dotenv import load_dotenv
load_dotenv("../../.env")

url = os.getenv("POLYMARKET_WEBSOCKET_URL")
api_key = os.getenv("POLYMARKET_API_KEY")
api_secret = os.getenv("POLYMARKET_API_SECRET")
api_passphrase = os.getenv("POLYMARKET_API_PASSPHRASE")

asset_ids = [
    "97212124472656863524759471926817043433361174058046518215176297401726819547323",
]
condition_ids = [] # no really need to filter by this one

auth = {"apiKey": api_key, "secret": api_secret, "passphrase": api_passphrase}

listener = WebSocketListener(url, asset_ids, queue=Queue())
listener.run()



