from datetime import datetime
from bs4 import BeautifulSoup
from lc_app.core.scrapers.models import Article
from lc_app.core.scrapers.scraper import NewsScraper

class FTScraper(NewsScraper):
    """
    Scraper for Financial Times articles.
    """

    def __init__(self, ticker: str):
        self.ticker = ticker
        self.base_url = "https://www.ft.com"
        self.search_url = f"{self.base_url}/search?q={ticker}"

    async def scrape(self) -> list[Article]:
        """
        Scrape news articles using playwright and return a list of dictionaries with the article title, url, and content.
        """
        content = await self.scrape_webpage(
            self.search_url,
            wait_for="div.o-teaser__content",
        ) 
        if not content:
            return []
        soup = BeautifulSoup(content, "html.parser")
        articles = soup.find_all("div", class_="o-teaser__content")
        news_data = []
        for article in articles:
            title = article.find("a").get_text()
            url = article.find("a")["href"]
            if not url.startswith("http"):
                url = f"{self.base_url}{url}"
            content = article.find("p").get_text() if article.find("p") else ""
            news_data.append(
                Article(
                    title=title,
                    url=url,
                    content=content,
                    ticker=self.ticker,
                    date=datetime.now(),
                    system="Financial Times",
                )
            )
        return news_data