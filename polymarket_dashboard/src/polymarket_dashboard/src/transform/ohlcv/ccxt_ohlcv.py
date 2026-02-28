import asyncio
import numpy as np
from polymarket_dashboard.src.ohlcv.ccxt_ohlcv import CcxtApi


async def process(ticker: str, data: list):
    return [
        {
            "timestamp": i[0],
            "open": i[1],
            "high": i[2],
            "low": i[3],
            "close": i[4],
            "volume": i[5],
            "ticker": ticker,
            "datetime": np.datetime64(i[0], "ms").astype("datetime64[s]").item().isoformat(),
        }
        for i in data
    ]


async def _ohlcv_parser(ohlcv_queue: asyncio.Queue, output_queue: asyncio.Queue):
    try:
        while True:
            ticker, data = await ohlcv_queue.get()
            if isinstance(data, Exception):
                print(f"Error fetching OHLCV for {ticker}: {data}")
            else:
                processed_ohlcv = await process(ticker, data)
                await output_queue.put(processed_ohlcv)

            ohlcv_queue.task_done()
    except asyncio.CancelledError:
        print("OHLCV parser cancelled.")
    finally:
        ohlcv_queue.task_done()


async def ohlcv_parser(
    client: CcxtApi,
    ohlcv_queue: asyncio.Queue,
    logger,
    max_workers: int = 4,
) -> asyncio.Queue:
    """Parse OHLCV data for a list of tokens and store results in an output queue.
    
    Args:
    ----
        client (CcxtApi): An instance of the CcxtApi class for fetching OHLCV data.
        timeframe (Timeframe): The timeframe for the OHLCV data (e.g., "1h", "1d", etc.).
        tokens (list[str]): A list of token symbols to fetch OHLCV data for.
        since (int): Timestamp in milliseconds to fetch data since.
        limit (int): Maximum number of OHLCV entries to fetch per token.
        until (int, optional): Timestamp in milliseconds to fetch data until. Defaults to None.
        max_workers (int, optional): Maximum number of concurrent worker tasks. Defaults to 4
    Returns:
    -------
        asyncio.Queue: An output queue containing processed OHLCV data for each token.
    """
    output_queue = asyncio.Queue()

    await client.exchange.close()
    workers = [
        asyncio.create_task(_ohlcv_parser(ohlcv_queue, output_queue))
        for _ in range(max_workers)
    ]

    logger.info(f"Started {max_workers} OHLCV parser workers.")

    await ohlcv_queue.join()
    for w in workers:
        w.cancel()
    await asyncio.gather(*workers, return_exceptions=True)

    return output_queue
