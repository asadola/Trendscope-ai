from abc import ABC
from playwright.sync_api import sync_playwright


class DynamicCrawler(ABC):
    browser_name = "chromium"

    def with_browser(self, func):
        with sync_playwright() as p:
            browser = getattr(p, self.browser_name).launch(headless=True)
            page = browser.new_page()
            try:
                return func(page)
            finally:
                browser.close()
