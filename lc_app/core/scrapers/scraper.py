import asyncio
from abc import ABC, abstractmethod

from lc_app.core.scrapers.models import Article


class NewsScraper(ABC):
    """A base class for news scrapers."""

    @abstractmethod
    async def scrape(self) -> list[Article]:
        """Scrape news articles and return a list of dictionaries with the article title, url, and content."""
        raise NotImplementedError("Subclasses must implement this method.")

    def sync_scrape(self) -> list[Article]:
        """Synchronously scrape news articles and return a list of dictionaries with the article title, url, and content."""
        asyncio.run(self.scrape())
