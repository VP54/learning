import asyncio
from polymarket_dashboard.src.news.base import Scraper
from polymarket_dashboard.src.config.types import ResponseJson


class ByBitAnnouncmentScraper(Scraper):
    """Bybit Scraper."""
    def __init__(self, logger, max_concurrent_requests: int=10, headers: dict=None):
        """Init class.
        
        Args:
        ----
            logger: logger to use
            max_concurrent_requests (int): max requests for semaphore
        """
        self.base_url = 'https://announcements.bybit.com/x-api/announcements/api/search/v1/index/announcement-posts_en'
        self.headers = headers or {
            "accept": "application/json",
            "accept-language": "en-US,en;q=0.9,cs;q=0.8",
            "content-type": "application/json;charset=UTF-8",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
        }
        self.logger = logger
        super().__init__(logger=logger, max_concurrent_requests=max_concurrent_requests)

    async def _get_data(self, page_num: int) -> dict:
        """Get data for request.
        
        Args:
        ----
            page_num (int): page number
        
        Returns:
        -------
            dict
        """
        return {"data": {"query": "", "page": page_num, "hitsPerPage": 20}}

    async def scrape_announcements(self, num_pages: int) -> list[ResponseJson]:
        """Scrape announcements.
        
        Args:
        ----
            num_pages (int): number of pages to scrape.
            
        Returns:
        -------
            list[ResponseJson]
        """
        tasks = [
                self.post_request(url=self.base_url, headers=self.headers, data=await self._get_data(page_num=page))
                for page in range(0, num_pages)
        ]
        responses = await asyncio.gather(*tasks)
        await self.close()
        return responses
        


if __name__ == "__main__":
    import logging
    logging.basicConfig(encoding='utf-8', level=logging.DEBUG, filename='example.log', )
    logger = logging.getLogger("test")

    client = ByBitAnnouncmentScraper(logger=logger, max_concurrent_requests=10)
    responses_bybit = asyncio.run(client.scrape_announcements(num_pages=2))
    