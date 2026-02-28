import asyncio
from polymarket_dashboard.src.news.base import Scraper
from polymarket_dashboard.src.config.types import ResponseJson
from polymarket_dashboard.src.config.enum import BinanceNewsCategory


class BinanceAnnouncmentScraper(Scraper):
    """Binance Scraper."""
    def __init__(self, logger, max_concurrent_requests: int = 10):
        """Init class.
        
        Args:
        ----
            logger: logger to use
            max_concurrent_requests (int): max requests for semaphore
        """
        self.base_url = "https://www.binance.com/bapi/apex/v1/public/apex/cms/article/list/query?type=1"
        self.logger = logger
        self.max_concurrent_requests = max_concurrent_requests
        super().__init__(logger=logger, max_concurrent_requests=max_concurrent_requests)

    async def scrape_announcements(self, category_id: BinanceNewsCategory, num_pages: int) -> list[ResponseJson]:
        """Scrape announcements.
        
        Args:
        ----
            category_id (int): category number
            num_pages (int): number of pages to scrape
            
        Returns:
        -------
            list[ResponseJson]
        """
        tasks = [
                self.get_request(url=f"{self.base_url}&pageNo={page}&pageSize=10&catalogId={category_id}")
                for page in range(1, num_pages + 1)
        ]
        self.logger.info(f"Num tasks: {len(tasks)}")
        results = await asyncio.gather(*tasks)
        await self.close()
        return results


if __name__ == "__main__":
    import logging
    logging.basicConfig(encoding='utf-8', level=logging.DEBUG, filename='example.log', )
    logger = logging.getLogger("test")
    binance_category = BinanceNewsCategory.LISTING

    client = BinanceAnnouncmentScraper(logger = logger, max_concurrent_requests=2)

    responses_binance = asyncio.run(client.scrape_announcements(num_pages=2, category_id=binance_category))
    
    import os
    with open("./sample_data/raw_news_binance.json", "w") as f:
        import json
        json.dump(responses_binance, f)