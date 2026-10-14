"""IR Assignment 4 - Implement a simple web crawler (using Scrapy).

Problem statement: starting from a seed URL, download pages, follow the links
breadth-first up to a depth limit, stay on the same site, skip repeated URLs and
record each page's title and number of links.

New lib used: scrapy (pip install scrapy / uv sync). Scrapy handles downloading,
the request queue and duplicate filtering; we only write the spider's parse().
Standard library: http.server + threading (a local test website, so no internet).

Driver: starts a local demo site of 6 pages, crawls it from the home page with
max depth 2 and prints what was crawled. No input is taken at runtime.
"""

import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

import scrapy
from scrapy.crawler import CrawlerProcess

# ---- demo website: path -> html ---------------------------------------------
SITE = {
    "/": '<title>Home</title><a href="/about">About</a> <a href="/news">News</a> <a href="http://other.example/x">External</a>',
    "/about": '<title>About</title><a href="/">Home</a> <a href="/team">Team</a>',
    "/news": '<title>News</title><a href="/news/1">Story 1</a> <a href="/about">About</a>',
    "/team": '<title>Team</title><a href="/deep">Deep page</a>',
    "/news/1": "<title>Story 1</title><p>No links here</p>",
    "/deep": "<title>Too deep</title>",
}


class SiteHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        page = SITE.get(self.path)
        self.send_response(200 if page else 404)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write((page or "<title>404</title>").encode())

    def log_message(self, *args):  # keep the output clean
        pass


# ---- crawler ----------------------------------------------------------------
pages = []  # one record per crawled page, filled by the spider


class SimpleCrawler(scrapy.Spider):
    name = "simple_crawler"
    allowed_domains = ["127.0.0.1"]  # stay on this site (external links are dropped)

    def __init__(self, start_url, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [start_url]

    def parse(self, response):
        links = response.css("a::attr(href)").getall()
        pages.append({
            "url": response.url,
            "depth": response.meta["depth"],
            "title": (response.css("title::text").get() or "").strip(),
            "links": len(links),
        })
        for href in links:
            yield response.follow(href, callback=self.parse)  # repeats are skipped by Scrapy


SETTINGS = {
    "DEPTH_LIMIT": 2,                 # max link-hops from the seed page
    "ROBOTSTXT_OBEY": False,          # our local demo site has no robots.txt
    "CONCURRENT_REQUESTS": 1,         # one page at a time, so output order is stable
    "DEPTH_PRIORITY": 1,              # the next three lines make the crawl breadth-first
    "SCHEDULER_DISK_QUEUE": "scrapy.squeues.PickleFifoDiskQueue",
    "SCHEDULER_MEMORY_QUEUE": "scrapy.squeues.FifoMemoryQueue",
    "LOG_LEVEL": "ERROR",
}


def main():
    server = HTTPServer(("127.0.0.1", 0), SiteHandler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{server.server_port}"

    process = CrawlerProcess(settings=SETTINGS)
    process.crawl(SimpleCrawler, start_url=base + "/")
    process.start()  # runs the crawl and blocks until it finishes
    server.shutdown()

    print(f"Crawled {len(pages)} pages (max depth 2) from {base}/")
    for p in sorted(pages, key=lambda p: (p["depth"], p["url"])):
        path = p["url"].replace(base, "") or "/"
        print(f"{'  ' * p['depth']}[d{p['depth']}] {path:<10} title={p['title']!r:<10} links={p['links']}")
    crawled = {p["url"].replace(base, "") for p in pages}
    print("Not crawled (beyond depth limit):", sorted(set(SITE) - crawled))


if __name__ == "__main__":
    main()
