from app.crawlers.dynamic_base import DynamicCrawler
from app.crawlers.base import BaseCrawler
from app.models.raw_event import RawEvent


class YouTubeTrendingCrawler(BaseCrawler, DynamicCrawler):
    name = "youtube_trending"

    def crawl(self):
        def run(page):
            url = "https://www.youtube.com/feed/trending"
            page.goto(url, timeout=90000)
            html = page.content()
            with open("yt_debug.html", "w", encoding="utf-8") as f:
                f.write(html)

            print("Saved yt_debug.html")

            # give YouTube time to settle
            page.wait_for_timeout(5000)

            # force scroll to trigger lazy loading
            for _ in range(3):
                page.mouse.wheel(0, 3000)
                page.wait_for_timeout(2000)

            # try multiple selectors (YouTube changes often)
            selectors = [
                "ytd-rich-item-renderer",
                "ytd-video-renderer",
                "a#video-title",
            ]

            items = []
            for sel in selectors:
                items = page.query_selector_all(sel)
                if items:
                    break

            events = []

            for item in items[:30]:
                # handle both container and direct anchor cases
                title_el = (
                    item.query_selector("a#video-title")
                    if hasattr(item, "query_selector")
                    else item
                )

                if not title_el:
                    continue

                title = title_el.inner_text().strip()
                href = title_el.get_attribute("href")

                if not title or not href:
                    continue

                if not href.startswith("http"):
                    href = "https://youtube.com" + href

                events.append(
                    RawEvent(
                        source=self.name, url=href, title=title, metadata={}
                    )
                )

            return events

        return self.with_browser(run)
