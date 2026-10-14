"""IR Assignment 4 - Implement a simple web crawler.

Problem statement: starting from a seed URL, download pages, extract the links, and
visit them breadth-first up to a depth limit, staying on the same site, avoiding
repeats and recording each page's title and outgoing links.

New libs used (all standard library): urllib (download + URL joining), html.parser
(link/title extraction), http.server + threading (a local test website so the
crawl needs no internet).

Driver: starts a local demo site of 6 pages on a free port, crawls it from the
home page with max depth 2 and prints the crawl tree. No input is taken at runtime.
"""

import threading
from collections import deque
from html.parser import HTMLParser
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urldefrag, urljoin, urlparse
from urllib.request import urlopen

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
class PageParser(HTMLParser):
    """Collects the <title> text and all <a href> links of one page."""

    def __init__(self):
        super().__init__()
        self.links, self.title, self._in_title = [], "", False

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            href = dict(attrs).get("href")
            if href:
                self.links.append(href)
        self._in_title = tag == "title"

    def handle_data(self, data):
        if self._in_title:
            self.title += data

    def handle_endtag(self, tag):
        self._in_title = False


def crawl(seed, max_depth=2):
    """Breadth-first crawl. Returns {url: (depth, title, [links])}."""
    site = urlparse(seed).netloc
    queue, visited, result = deque([(seed, 0)]), {seed}, {}
    while queue:
        url, depth = queue.popleft()
        try:
            html = urlopen(url, timeout=5).read().decode(errors="replace")
        except OSError:
            continue
        parser = PageParser()
        parser.feed(html)
        links = [urldefrag(urljoin(url, href))[0] for href in parser.links]
        result[url] = (depth, parser.title.strip(), links)
        if depth < max_depth:
            for link in links:
                if urlparse(link).netloc == site and link not in visited:  # same site, not seen
                    visited.add(link)
                    queue.append((link, depth + 1))
    return result


def main():
    server = HTTPServer(("127.0.0.1", 0), SiteHandler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{server.server_port}"

    pages = crawl(base + "/", max_depth=2)
    print(f"Crawled {len(pages)} pages (max depth 2) from {base}/")
    for url, (depth, title, links) in pages.items():
        print(f"{'  ' * depth}[d{depth}] {url.replace(base, '') or '/':<10} title={title!r:<10} links={len(links)}")
    skipped = {"/deep"} - {u.replace(base, "") for u in pages}
    print("Not crawled (beyond depth limit):", sorted(skipped))
    server.shutdown()


if __name__ == "__main__":
    main()
