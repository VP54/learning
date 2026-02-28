from abc import ABC, abstractmethod


class Scraper(ABC):

    @abstractmethod
    def scrape_announcements():
        raise NotImplementedError("Implement scrape_announcements method!")
