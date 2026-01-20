import json
import ast
from websocket import WebSocketApp
from polymarket_dashboard.src.config.logger import logger
from polymarket_dashboard.src.config.enum import Exchange


class WebSocketListener:
    """Simple websocket listener fo Polymarket.

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
    def __init__(self, url, asset_ids, queue, loop, market_channel, logger=logger):
        self.url = url
        self.asset_ids = asset_ids
        self.queue = queue
        self.loop = loop
        self.market_channel = market_channel
        self.logger = logger

        logger.info(
            f"Connecting to Polymarket: url: {self.url}, asset_ids: {self.asset_ids}, queue: {self.queue}"
            f"Loop: {self.loop}, market_channel: {self.market_channel}"
        )

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

        message = ast.literal_eval(message)

        if message['event_type'] == "book":
            logger.debug(f"POLYMARKET - {message} \t {self.queue.qsize()}")
            self.loop.call_soon_threadsafe(self.queue.put_nowait, (Exchange.Polymarket.value, message))

    def on_error(self, ws, error):
        print("[WS] Error:", error)

    def on_close(self, ws, code, msg):
        print("[WS] Closed:", code, msg)

    async def run(self):
        self.ws.run_forever(ping_interval=None)
