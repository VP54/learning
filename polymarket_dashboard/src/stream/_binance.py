import asyncio
import os
import polars as pl
import threading
import asyncio
import websockets
import json
import time


def heavy_calc(message):
    open = message.get("o")
    high = message.get("h")
    low = message.get("l")
    close = message.get("c")

    return open * high *low + close


async def binance_price_ws(queue, symbols, throttle=0.3):
    streams = "/".join(f"{s}@ticker" for s in symbols)
    url = f"wss://fstream.binance.com/stream?streams={streams}"

    async with websockets.connect(url) as ws:
        print("Connected to Binance Futures Ticker WebSocket!")
        last_update = 0
        while True:
            msg = await ws.recv()
            now = time.time()
            if now - last_update >= throttle:
                last_update = now
                data = json.loads(msg)
                stream = data.get('stream')
                await queue.put(
                    (stream, data['data'])
                )


def transform_queue_message(queue, executor):
    loop = asyncio.get_event_loop()
    while True:
        data = queue.get()
        result = loop.run_in_executor(executor, heavy_calc, data)
        print(result)


async def main():
    symbols = ["btcusdt", "ethusdt", "bnbusdt"]
    import queue
    queue = queue.Queue()
    from concurrent.futures import ProcessPoolExecutor
    executor = ProcessPoolExecutor(max_workers=10)

    await asyncio.gather(
        binance_price_ws(queue, symbols),
        transform_queue_message(queue, executor),
    )



asyncio.run(main())