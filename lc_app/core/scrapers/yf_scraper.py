from datetime import datetime

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

from lc_app.core.scrapers.models import Article
from lc_app.core.scrapers.scraper import NewsScraper


class YahooFinanceNewsScraper(NewsScraper):
    """A class to scrape news articles from Yahoo Finance."""

    def __init__(self, ticker: str):
        self.ticker = ticker

    async def __scrape_webpage(self, url: str, wait_for: str) -> str:
        """scrape webpage using playwright and return the content."""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url)
            await page.wait_for_selector(wait_for)
            content = await page.content()
            await browser.close()
        return content

    async def scrape(self) -> list[Article]:
        """scrape news articles using playwright and return a list of dictionaries with the article title, url, and content."""
        content = await self.__scrape_webpage(
            f"https://finance.yahoo.com/quote/{self.ticker}/latest-news/",
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
                    date=datetime.now(),
                    published_at=published_at,
                    system="Yahoo Finance",
                )
            )
        return news_data

    # async with async_playwright() as p:
    #     browser = await p.chromium.launch(headless=True)
    #     page = await browser.new_page()
    #     await page.goto(f"https://finance.yahoo.com/quote/{ticker}/news?p={ticker}")
    #     await page.wait_for_selector("div.news-stream")
    #     content = await page.content()

    #     soup = BeautifulSoup(content, "html.parser")
    #     articles = soup.find_all("li", class_=lambda x: x and "story-item" in x)
    #     news_data = []
    #     for article in articles:
    #         title = article.find("h3").get_text()
    #         url = article.find("a")["href"]
    #         if not url.startswith("http"):
    #             url = f"https://finance.yahoo.com{url}"
    #         content = article.find("p").get_text() if article.find("p") else ""
    #         news_data.append({"title": title, "url": url, "content": content})
    #     await browser.close()
    # return news_data
