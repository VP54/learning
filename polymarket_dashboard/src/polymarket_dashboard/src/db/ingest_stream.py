import asyncio
import time
import sys
import datetime
from questdb.ingress import Sender, IngressError


async def insert_into_db(conf, table_name, queue, func, executor, logger):
    logger.info("Starting DB insert task...")
    with Sender.from_conf(conf) as sender:
        while True:
            message = await queue.get()
            logger.info(f"Received message: {message}")
            if message is None:
                break

            loop = asyncio.get_running_loop()
            result = await loop.run_in_executor(executor, func, message, logger)
            at = datetime.datetime.fromtimestamp(time.time(), datetime.timezone.utc)
            try:
                sender.row(table_name=table_name, columns=result, at=at)
            except IngressError as e:
                sys.stderr.write(f'Got error: {e}\n')

            queue.task_done()


# insert_into_db(conf=conf, table_name=table_name, payload=payload)


async def _insert_into_db(conf, table_name, queue, func, executor, logger):
    logger.info(f"Starting DB insert task for {table_name}...")
    with Sender.from_conf(conf) as sender:
        buffer = []
        last_flush = time.time()
        loop = asyncio.get_running_loop()

        while True:
            message = await queue.get()
            print(f"Received message: {message}")
            if message is None:
                # flush remaining messages
                if buffer:
                    at = datetime.datetime.now(datetime.timezone.utc)
                    for row in buffer:
                        sender.row(table_name=table_name, columns=row, at=at)
                queue.task_done()
                break

            # parse in executor
            result = await loop.run_in_executor(executor, func, message, logger)
            buffer.append(result)
            now = time.time()

            # flush triggers
            # logger.info(f"{table_name} - Buffer size: {len(buffer)} \t {now - last_flush}s flush")
            if len(buffer) >= 1000 or (now - last_flush) >= 0.1:
                at = datetime.datetime.now(datetime.timezone.utc)
                for row in buffer:
                    sender.row(table_name=table_name, columns=row, at=at)
                buffer.clear()
                last_flush = now

            queue.task_done()
