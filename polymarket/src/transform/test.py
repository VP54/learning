import os
import json
from queue import Queue
from websocket import WebSocketApp
from dotenv import load_dotenv


class WebSocketListener:
    """Websocket Listener to Polymarket.

    Example:
    -------
        MARKET_CHANNEL = "market"
        USER_CHANNEL = "user"
        load_dotenv("")

        url = os.getenv("POLYMARKET_WEBSOCKET_URL")
        api_key = os.getenv("POLYMARKET_API_KEY")
        api_secret = os.getenv("POLYMARKET_API_SECRET")
        api_passphrase = os.getenv("POLYMARKET_API_PASSPHRASE")

        asset_ids = ["115172850081268399385975128465963399335156000901458077700537686348329692537170"]
        condition_ids = []
        auth = {"apiKey": api_key, "secret": api_secret, "passphrase": api_passphrase}
        listener = WebSocketListener(url, asset_ids, queue=Queue())
        listener.run()
    """
    def __init__(self, url: str, asset_ids: list[str], queue: Queue):
        """Initialize class.

        Args:
            url (str) - Polymarket URL
            asset_ids (list) - List of asset IDs. (check ws for asset ids)
            queue (Queue) - Queue - Queue to put messages to.
        """
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




if __name__ == "__main__":
    MARKET_CHANNEL = "market"
    USER_CHANNEL = "user"
    load_dotenv("../../.env")

    url = os.getenv("POLYMARKET_WEBSOCKET_URL")
    api_key = os.getenv("POLYMARKET_API_KEY")
    api_secret = os.getenv("POLYMARKET_API_SECRET")
    api_passphrase = os.getenv("POLYMARKET_API_PASSPHRASE")

    asset_ids = [
        "115172850081268399385975128465963399335156000901458077700537686348329692537170",
    ]
    condition_ids = [] # no really need to filter by this one

    auth = {"apiKey": api_key, "secret": api_secret, "passphrase": api_passphrase}

    listener = WebSocketListener(url, asset_ids, queue=Queue())

    listener.run()



