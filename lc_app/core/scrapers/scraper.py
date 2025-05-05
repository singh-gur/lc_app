import asyncio
from abc import ABC, abstractmethod
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
from lc_app.core.scrapers.models import Article


class NewsScraper(ABC):
    """A base class for news scrapers."""

    @abstractmethod
    async def scrape(self) -> list[Article]:
        """Scrape news articles and return a list of dictionaries with the article title, url, and content."""
        raise NotImplementedError("Subclasses must implement this method.")

    def sync_scrape(self) -> list[Article]:
        """Synchronously scrape news articles and return a list of dictionaries with the article title, url, and content."""
        return asyncio.run(self.scrape())

    async def scrape_webpage(self, url: str, wait_for: str, error_on_timeout: bool = True) -> str:
        """
        Scrape the content of a webpage using Playwright.

        This asynchronous method navigates to the specified URL, waits for a specific
        element to load, and retrieves the page's HTML content.

        Args:
            url (str): The URL of the webpage to scrape.
            wait_for (str): The CSS selector of the element to wait for before scraping.

        Returns:
            str: The HTML content of the webpage.

        Raises:
            playwright._impl._api_types.Error: If there is an issue with Playwright operations,
            such as navigation or selector waiting.

        Note:
            This method uses a headless Chromium browser for scraping.
        """
        """scrape webpage using playwright and return the content."""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            try:
                await page.goto(url)
                await page.wait_for_selector(wait_for, timeout=10000)
                content = await page.content()
            except PlaywrightTimeoutError as e:
                if error_on_timeout:
                    raise e
                else:
                    print(f"Error: {e}")
                    content = None
            finally:
                # Ensure the page is closed even if an error occurs
                await page.close()
                await browser.close()
        return content