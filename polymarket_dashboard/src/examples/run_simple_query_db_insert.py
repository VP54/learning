import asyncio
from polymarket_dashboard.src.stream.binance import binance_price_ws
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from polymarket_dashboard.src.db.ingest_stream import insert_into_db, parse_message

conf = (
    'http::addr=localhost:9000;'
    'username=admin;password=quest;'
    'auto_flush_rows=100;auto_flush_interval=1000;')
table_name = "trade_stream"
symbols = ["btcusdt"]
queue = asyncio.Queue()


async def main(conf, queue, symbols, table_name):
    executor = ProcessPoolExecutor(max_workers=10)
    db_task = asyncio.create_task(insert_into_db(conf, table_name, queue, parse_message, executor))
    await binance_price_ws(queue=queue, symbols=symbols)
    await queue.put(None)
    await db_task

asyncio.run(
    main(conf, queue, symbols, table_name)
)