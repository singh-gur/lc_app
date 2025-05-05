from datetime import datetime

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

from lc_app.core.scrapers.models import Article
from lc_app.core.scrapers.scraper import NewsScraper


class YahooFinanceNewsScraper(NewsScraper):
    """A class to scrape news articles from Yahoo Finance."""

    def __init__(self, ticker: str | None = None, topic: str | None = None):
        self.ticker = ticker
        self.topic = topic if topic else "latest-news"
        self.base_url = "https://finance.yahoo.com"
        if self.ticker:        
            self.news_url = f"{self.base_url}/quote/{self.ticker}/latest-news/"
        else:
            self.news_url = f"{self.base_url}/topic/{self.topic}"


    async def scrape(self) -> list[Article]:
        """scrape news articles using playwright and return a list of dictionaries with the article title, url, and content."""
        content = await self.scrape_webpage(
            self.news_url,
            wait_for="div.news-stream",
        )
        if not content:
            return []
        soup = BeautifulSoup(content, "html.parser")
        articles = soup.find_all("li", class_=lambda x: x and "story-item" in x)
        news_data = []
        for article in articles:
            title = article.find("h3").get_text()
            url = article.find("a")["href"]
            if not url.startswith("http"):
                url = f"https://finance.yahoo.com{url}"
            content = await self.__scrape_detailed_page(url)
            if not content:
                content = article.find("p").get_text() if article.find("p") else ""
            source_date = article.find("div", class_=lambda x: x and "publishing" in x)
            if source_date and len(source_date.contents) >= 3:
                source = source_date.contents[0].get_text().strip()
                published_at = source_date.contents[2].get_text().strip()
            news_data.append(
                Article(
                    title=title,
                    url=url,
                    content=content,
                    source=source,
                    ticker=self.ticker,
                    topic=self.topic,
                    date=datetime.now(),
                    published_at=published_at,
                    system="Yahoo Finance",
                )
            )
        return news_data
    
    async def __scrape_detailed_page(self, url: str) -> str | None:
        """scrape detailed page using playwright and return the content."""
        content = await self.scrape_webpage(url, wait_for="div.article")
        if not content:
            return None
        soup = BeautifulSoup(content, "html.parser")
        title = soup.find("div", class_=lambda x: x and "cover-title" in x).get_text()
        article_body = soup.find("div", class_=lambda x:x and "body" in x).get_text()
        return article_body
