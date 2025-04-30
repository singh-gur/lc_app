from typing import Any

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright


async def scrape_webpage(url: str, wait_for: str) -> str:
    """scrape webpage using playwright and return the content."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)
        await page.wait_for_load_state(wait_for)
        content = await page.content()
        await browser.close()
    return content


async def scrape_news_articles_for_tickers(ticker: str) -> list[dict[str, Any]]:
    """scrape news articles using playwright and return a list of dictionaries with the article title, url, and content."""
    content = await scrape_webpage(
        f"https://finance.yahoo.com/quote/{ticker}/latest-news/",
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
        news_data.append({"title": title, "url": url, "content": content})
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
