"""IR Assignment 4 (real website version) - Simple web crawler using Scrapy.

Problem statement: crawl a real site from a seed URL, breadth-first, up to a depth
and page limit, staying on the same domain, respecting robots.txt, and saving each
page's URL, title and link count.

New lib used: scrapy. Driver: crawls books.toscrape.com (a practice site built
for scraping), prints a summary and saves pages.json. Needs internet. No input
is taken at runtime. Only crawl sites that allow it (check their robots.txt).
"""

from urllib.parse import urlparse

import scrapy
from scrapy.crawler import CrawlerProcess

SEED_URL = "https://en.wikipedia.org/wiki/Picts"   # change this to crawl another site
MAX_DEPTH = 2
MAX_PAGES = 30

pages = []


class SimpleCrawler(scrapy.Spider):
    name = "simple_crawler"

    def __init__(self, start_url, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [start_url]
        self.allowed_domains = [urlparse(start_url).netloc]  # same site only

    def parse(self, response):
        if "text/html" not in response.headers.get("Content-Type", b"").decode():
            return                                           # skip images, pdfs, etc.
        links = response.css("a::attr(href)").getall()
        record = {
            "url": response.url,
            "depth": response.meta["depth"],
            "title": (response.css("title::text").get() or "").strip(),
            "links": len(links),
        }
        pages.append(record)
        yield record                                         # also saved to pages.json
        for href in links:
            yield response.follow(href, callback=self.parse)


SETTINGS = {
    "DEPTH_LIMIT": MAX_DEPTH,
    "CLOSESPIDER_PAGECOUNT": MAX_PAGES,   # hard stop after this many pages
    "ROBOTSTXT_OBEY": True,               # respect the site's robots.txt rules
    "DOWNLOAD_DELAY": 1,                  # wait 1 s between requests (be polite)
    "CONCURRENT_REQUESTS": 1,
    "USER_AGENT": "pict-lab-crawler (student project)",
    "DEPTH_PRIORITY": 1,                  # breadth-first order
    "SCHEDULER_DISK_QUEUE": "scrapy.squeues.PickleFifoDiskQueue",
    "SCHEDULER_MEMORY_QUEUE": "scrapy.squeues.FifoMemoryQueue",
    "FEEDS": {"pages.json": {"format": "json", "overwrite": True}},
    "LOG_LEVEL": "WARNING",
}


def main():
    process = CrawlerProcess(settings=SETTINGS)
    process.crawl(SimpleCrawler, start_url=SEED_URL)
    process.start()
    print(f"Crawled {len(pages)} pages from {SEED_URL}")
    for p in pages[:15]:
        print(f"[d{p['depth']}] {p['title'][:40]!r:<44} links={p['links']:<4} {p['url']}")


if __name__ == "__main__":
    main()
