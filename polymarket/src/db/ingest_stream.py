import asyncio
import time
from questdb.ingress import Sender, IngressError, TimestampNanos
import sys
import datetime


def parse_message(message, logger):
    logger.info(f"Parsing message: {message}")

    data = message[1]

    payload = {
        "symbol": data['s'],
        "open": float(data['o']),
        "volume": float(data['v']),
        "timestamp_binance": data['C']
    }
    logger.info(payload)
    return payload



async def insert_into_db(conf, table_name, queue, func, executor, logger):
    print("Starting DB insert task...")
    with Sender.from_conf(conf) as sender:
        while True:
            message = await queue.get()  # Await queue
            logger.info(f"Received message: {message}")
            if message is None:          # Sentinel to stop
                break

            loop = asyncio.get_running_loop()
            result = await loop.run_in_executor(executor, func, message, logger)

            at = datetime.datetime.fromtimestamp(time.time(), datetime.timezone.utc)
            try:
                sender.row(table_name=table_name, columns=result, at=at)
            except IngressError as e:
                sys.stderr.write(f'Got error: {e}\n')

            queue.task_done()  # Mark processed



# insert_into_db(conf=conf, table_name=table_name, payload=payload)