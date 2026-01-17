from typing import Callable
import asyncio


def transform_queue_message(queue, executor, func: Callable):
    loop = asyncio.get_event_loop()
    while True:
        data = queue.get()
        result = loop.run_in_executor(executor, func, data)
        print(result)