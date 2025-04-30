from lc_app.core.scrapers.models import Article


class NewsScraper:
    """A base class for news scrapers."""

    async def scrape(self) -> list[Article]:
        """Scrape news articles and return a list of dictionaries with the article title, url, and content."""
        raise NotImplementedError("Subclasses must implement this method.")
