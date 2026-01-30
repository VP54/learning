import logging
import os
import asyncio
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from dotenv import load_dotenv
from polymarket_dashboard.src.utils.setup_table import create_table_if_not_exists
from polymarket_dashboard.src.config.query import (
    INDEX_BINANCE_TRADES, SCHEMA_BINANCE_TRADES, PARTITION_BINANCE_BY,
    SCHEMA_POLYMARKET_TRADES, INDEX_POLYMARKET_TRADES, PARTITION_POLYMARKET_BY
)
from polymarket_dashboard.src.stream.polymarket import WebSocketListener
from polymarket_dashboard.src.stream.binance import binance_price_ws
from polymarket_dashboard.src.config.logger import create_logger
from polymarket_dashboard.src.db.ingest_stream import _insert_into_db
from polymarket_dashboard.src.transform.router import route_message
from polymarket_dashboard.src.config.enum import DatabaseTableNames
from polymarket_dashboard.src.utils.init_event_date import get_initial_datetime
from polymarket_dashboard.src.polymarket_api.add_asset_id import add_asset_ids



logger = create_logger(logging.WARNING)
conf = (
    'http::addr=localhost:9000;'
    'username=admin;password=quest;'
    'auto_flush_rows=100;auto_flush_interval=1000;'
)
table_name = "trade_stream"
symbols = ["btcusdt"]
queue = asyncio.Queue()
MARKET_CHANNEL = "market"
USER_CHANNEL = "user"
load_dotenv('../.env')
url = os.getenv("POLYMARKET_WEBSOCKET_URL")
symbols = ["btcusdt"]


import asyncio
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=1)  # single thread for WebSocket

async def run_listener(listener: WebSocketListener):
    loop = asyncio.get_running_loop()
    # run the blocking run_forever in a thread, but await it in asyncio
    await loop.run_in_executor(executor, listener.ws.run_forever, None)  # ping_interval=None


async def asset_id_updater(listener, logger):
    while True:
        try:
            new_asset_ids, _ = await add_asset_ids(
                list(listener.asset_ids),
                logger=logger,
            )
            await listener.add_asset_ids(new_asset_ids)
        except Exception:
            logger.exception("asset_id updater failed")

        await asyncio.sleep(30)  # or whatever cadence


async def main():
    init_asset_ids = []
    loop = asyncio.get_running_loop()
    _now = get_initial_datetime()
    init_asset_ids, asset_id_timestamp_dict = await add_asset_ids(init_asset_ids, now=_now, logger=logger)
    # Queues
    binance_queue = asyncio.Queue(maxsize=10_000)
    poly_queue = asyncio.Queue(maxsize=2_000)

    # Executor for CPU-bound parsing
    listener = WebSocketListener(url, init_asset_ids, queue=poly_queue, loop=loop, market_channel=MARKET_CHANNEL)
    executor = ProcessPoolExecutor(max_workers=4)

    tasks = [
        asyncio.create_task(asset_id_updater(listener, logger)),
        asyncio.create_task(binance_price_ws(queue=binance_queue, symbols=symbols, throttle=0.001)),
        asyncio.create_task(_insert_into_db(conf, DatabaseTableNames.Binance.value, binance_queue, route_message, executor, logger)),
        asyncio.create_task(run_listener(listener)),
        asyncio.create_task(_insert_into_db(conf, DatabaseTableNames.Polymarket.value, poly_queue, route_message, executor, logger)),
    ]

    await asyncio.gather(*tasks)

minute = 40
modulo = 15
_minute = modulo - minute % modulo - 1 + minute
print(_minute)

if __name__ == "__main__":
    from polymarket_dashboard.src.config.paths import MESSAGE_HANDLER_PATH
    from polymarket_dashboard.src.utils.message_handler import init_handlers
    from polymarket_dashboard.src.transform.polymarket import parse_polymarket_message
    from polymarket_dashboard.src.transform.binance import parse_binance_message
    init_handlers(MESSAGE_HANDLER_PATH)

    create_table_if_not_exists(
        table_name="binance_trades",
        schema=SCHEMA_BINANCE_TRADES,
        partition_by=PARTITION_BINANCE_BY,
        index_columns=INDEX_BINANCE_TRADES,
    )

    create_table_if_not_exists(
        table_name="polymarket_trades",
        schema=SCHEMA_POLYMARKET_TRADES,
        partition_by=PARTITION_POLYMARKET_BY,
        index_columns=INDEX_POLYMARKET_TRADES,
    )

    asyncio.run(main())

from questdb.ingress import Sender, IngressError
import datetime
with Sender.from_conf(conf) as sender:
    sender.row(table_name=table_name, columns={"exchange": "POLYMARKET"}, at=datetime.datetime.now(datetime.timezone.utc))
