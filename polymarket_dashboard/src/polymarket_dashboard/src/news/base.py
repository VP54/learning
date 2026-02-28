from abc import ABC, abstractmethod
import asyncio
import json
import aiohttp
from polymarket_dashboard.src.config.types import ResponseJson


class Scraper(ABC):
    """Base Scraper."""
    def __init__(self, logger: any, max_concurrent_requests: int) -> None:
        """Init class.
        
        Args:
        ----
            logger (any): logger to use
            max_concurrent_requests (int): semaphore param

        Returns:
        -------
            None    
        """
        self.logger = logger
        self.max_concurrent_requests = max_concurrent_requests
        self._session: aiohttp.ClientSession | None = None
        self.semaphore = asyncio.Semaphore(max_concurrent_requests)

    async def start(self) -> None:
        """Init session so its just once for whole Scraper."""
        if not self._session:
            self.logger.info(f"Starting session.")
            self._session = aiohttp.ClientSession()

    async def close(self) -> None:
        """Close aiohttp session."""
        if self._session:
            self.logger.info(f"Closing session.")
            self._session.close()
            self._session = None
    
    async def get_request(self, url: str) -> ResponseJson:
        """Make GET request.
        
        Args:
        ----
            url (str): url to make request to.

        Returns:
        -------
            dict
        """
        await self.start()
        async with self.semaphore:
            async with self._session.get(url) as response:
                self.logger.info(f"Status: {response.status}")
                return await response.json()
                
    async def post_request(self, url: str, headers: dict, data: dict) -> ResponseJson:
        """Make POST request.
        
        Args:
        ----
            url (str): url to make request to.
            headers (dict): request headers.
            data (dict): data to post

        Returns:
        -------
            dict
        """
        await self.start()
        async with self.semaphore:
            async with self._session.post(url, headers=headers, data=json.dumps(data)) as response:
                print(response)
                self.logger.info(f"Status: {response.status}")
                return await response.json()
                
    @abstractmethod
    async def scrape_announcements():
        raise NotImplementedError("Implement scrape_announcements method!")
