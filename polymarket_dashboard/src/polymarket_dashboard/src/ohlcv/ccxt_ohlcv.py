import asyncio
import ccxt.async_support as ccxt_client
from polymarket_dashboard.src.config.types import Exchange
from polymarket_dashboard.src.config.enum import Timeframe


class CcxtApi:
    """A client for fetching OHLCV data using the CCXT library.

    Note:
    -----
        Quotes start from the next first interval. For example,
        if you fetch 1h data at 10:30, the first quote will be for the 
        interval starting at 11:00. (if 1hr).
    
    Example:
    -------
        ```python
        client = CcxtApi(Exchange.BINANCE, logger=logger)
        current_prices = await client.fetch_ohlcv_current_prices(["BTC/USDT", "ETH/USDT"], )
        ohlcv = await client.fetch_ohlcv_list("BTC/USDT", timeframe="1h", since=1622505600000, limit=100)
        ```
    """
    def __init__(self, exchange_name: Exchange, logger) -> None:
        """Initialize the CCXT client with the specified exchange.
        
        Args:
        ----
            exchange_name (Exchange): The name of the exchange to connect to.
            logger: Logger instance for logging information and errors.

        Returns:
        -------
            None
        """
        self.logger = logger
        self.exchange_name = exchange_name.value.lower()
        self.exchange = getattr(ccxt_client, self.exchange_name)()

    async def create_time_interval(self, since, until, timeframe, limit):
        """Create a list of time intervals based on the specified parameters.

        Args:
            since (int): The starting timestamp in milliseconds.
            until (int): The ending timestamp in milliseconds.
            timeframe (str): The timeframe for the intervals (e.g., "1h", "1d").

        Returns:
            list: A list of time intervals as tuples (start_time, end_time).
        """
        intervals = []
        step_ms = self.exchange.parse_timeframe(timeframe)
        current_time = since

        while current_time < until:
            next_time = current_time + step_ms * limit
            intervals.append((current_time, next_time))
            current_time = next_time

        self.logger.info(f"Created {len(intervals)} time intervals for fetching OHLCV data.")

        return intervals

    async def _fetch_ohlcv(self, symbol: str, timeframe: str, since: int = None, limit: int = None) -> list:
        """Fetch OHLCV data for a specific symbol and timeframe.
        
        Args:
        ----
            symbol (str): The trading pair symbol (e.g., "BTC/USDT").
            timeframe (str): The timeframe for the OHLCV data (e.g., "1h", "1d").
            since (int, optional): Timestamp in milliseconds to fetch data since. Defaults to None.
            limit (int, optional): Maximum number of OHLCV entries to fetch. Defaults to None.
        Returns:
        -------
            list: A list of OHLCV data points, where each point is a list containing [timestamp, open, high, low, close, volume].
        """
        ohlcv_data = await self.exchange.fetch_ohlcv(symbol, timeframe=timeframe, since=since, limit=limit)
        self.logger.debug(f"Fetched {len(ohlcv_data)} OHLCV entries for {symbol} at timeframe {timeframe} since {since} with limit {limit}.")
        return ohlcv_data
    
    async def _worker(self, queue, output_queue, results, timeframe, limit):
        """Worker function to fetch OHLCV data from the queue and store results.
        
        Args:
        ----
            queue (asyncio.Queue): The queue containing tasks for fetching OHLCV data.
            results (list): A list to store the fetched OHLCV data or exceptions.
            timeframe (str): The timeframe for the OHLCV data (e.g., "1h", "1d").
            limit (int): Maximum number of OHLCV entries to fetch.

        Returns:
        -------

            None
        """        
        while True:
            try:
                token, start = await queue.get()
            except asyncio.CancelledError:
                break

            try:
                data = await self._fetch_ohlcv(
                    symbol=token,
                    timeframe=timeframe,
                    since=start,
                    limit=limit,
                )
                asyncio.wait(.1)
                await output_queue.put((token, data))
            except Exception as e:
                await output_queue.put((token, e))
            finally:
                queue.task_done()
    
    async def fetch_ohlcv_list(
        self,
        tokens: list,
        timeframe: str,
        since: int,
        until: int,
        limit: int = None,
        max_workers: int = 10,  # tune 5–15
    ) -> list:
        """Fetch OHLCV data for a list of tokens concurrently using a worker pool.
        Args:
        ----

            tokens (list): A list of trading pair symbols (e.g., ["BTC/USDT", "ETH/USDT"]).
            timeframe (str): The timeframe for the OHLCV data (e.g., "1h", "1d").
            since (int): Timestamp in milliseconds to fetch data since.
            until (int): Timestamp in milliseconds to fetch data until.
            limit (int, optional): Maximum number of OHLCV entries to fetch. Defaults to None.
            max_workers (int, optional): Maximum number of concurrent workers. Defaults to 10.
        Returns:
        -------
            list: A list of OHLCV data for each token, where each entry corresponds to the OHLCV data for a specific token.
            """

        until = until or int(self.exchange.milliseconds())
        intervals = await self.create_time_interval(since=since, until=until, timeframe=timeframe, limit=limit)
        queue = asyncio.Queue()
        output_queue = asyncio.Queue()
        results = []

        for token in tokens:
            for start, _ in intervals:
                await queue.put((token,  start * 1000))

        self.logger.info(f"Enqueued {queue.qsize()} tasks for fetching OHLCV data for tokens: {tokens}.")

        workers = [asyncio.create_task(self._worker(queue, output_queue, results, timeframe, limit)) for _ in range(max_workers)]
        self.logger.info(f"Started {max_workers} workers: {workers} for fetching OHLCV data.")

        await queue.join()
        for w in workers:
            w.cancel()

        await asyncio.gather(*workers, return_exceptions=True)

        return output_queue

    async def fetch_ohlcv_markets(self) -> dict:
        """ Fetch the available markets from the exchange."""
        markets = await self.exchange.load_markets()
        return markets

    async def fetch_ohlcv_current_prices(self, tickers: list) -> dict:
        """Fetch the current prices for a list of tickers.

        Args:
        ----
            tickers (list): A list of trading pair symbols (e.g., ["BTC/USDT", "ETH/USDT"]).
        
        Returns:
        -------
            dict: A dictionary mapping each ticker to its current price.
        """
        markets = await self.fetch_ohlcv_markets()
        return {
            ticker: markets.get(ticker, None) for ticker in tickers
        }
    
    async def close(self):
        await self.exchange.close()


# if __name__ == "__main__":
    # async def main():
    #     client = CcxtApi(Exchange.Binance)  # Exchange.BINANCE
    #     # current_prices = await client.fetch_ohlcv_current_prices(["BTC/USDT", "ETH/USDT"])
    #     # print("Current Prices:", current_prices)
    #     timeframe = Timeframe.H1.value
    #     output_ohlcv_queue = await client.fetch_ohlcv_list(["BTC/USDT"], timeframe=timeframe, since=1622505640000, limit=100, until=1622505640000 + 3600 * 1000 * 24)  # Fetch 1 day of hourly data starting from June 1, 2021
    #     print("OHLCV Data:", output_ohlcv_queue)
    #     await client.close()

    # asyncio.run(main())

    