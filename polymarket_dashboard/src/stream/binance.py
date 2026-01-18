import time
import json
import websockets


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
                print((stream, data['data']))
                await queue.put(
                    (stream, data['data'])
                )
