"""CSDF Mini-project - web version of the image forensics tool.

Problem statement: upload an image (it is saved in the images/ folder) or pick one already there,
and see the forensic report in the browser, optionally compared with an original image.
Libs used (standard library only): http.server, json, webbrowser, pathlib, plus forensics.py.
Driver: run the file; index.html opens in the browser at http://localhost:8000. Ctrl+C stops it.
"""

import json
import mimetypes
import re
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

from forensics import analyse, compare_images
from make_samples import IMAGES, make_samples

PORT = 8000
ALLOWED = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"}
MAX_BYTES = 20 * 1024 * 1024
PAGE = Path(__file__).parent / "index.html"


def safe_name(name):
    """Keep only letters, digits, dot, dash and underscore so the file name is safe on Windows too."""
    path = Path(name.replace("\\", "/")).name
    stem = re.sub(r"[^A-Za-z0-9_-]+", "_", Path(path).stem).strip("_") or "image"
    return stem + Path(path).suffix.lower()


def image_names():
    return sorted(p.name for p in IMAGES.iterdir() if p.suffix.lower() in ALLOWED)


def free_name(name):
    path = IMAGES / name
    number = 1
    while path.exists():
        path = IMAGES / f"{Path(name).stem}_{number}{Path(name).suffix}"
        number += 1
    return path


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = unquote(urlparse(self.path).path)
        if path == "/":
            self.reply(200, "text/html; charset=utf-8", PAGE.read_bytes())
        elif path == "/images":
            self.reply(200, "application/json", json.dumps(image_names()).encode())
        elif path.startswith("/images/") and Path(path).name in image_names():
            file = IMAGES / Path(path).name
            self.reply(200, mimetypes.guess_type(file.name)[0] or "application/octet-stream", file.read_bytes())
        else:
            self.reply(404, "text/plain", b"Not found")

    def do_POST(self):
        size = int(self.headers.get("Content-Length", 0))
        if size > MAX_BYTES:
            return self.send_json({"error": "File is too large (limit 20 MB)."}, 413)
        data = self.rfile.read(size)
        url = urlparse(self.path)
        try:
            if url.path == "/upload":
                names = parse_qs(url.query).get("name")
                if not names:
                    return self.send_json({"error": "Missing file name."}, 400)
                self.send_json(self.upload(names[0], data))
            elif url.path == "/analyse":
                self.send_json(self.analyse(json.loads(data)))
            else:
                self.reply(404, "text/plain", b"Not found")
        except (KeyError, ValueError):
            self.send_json({"error": "Bad request."}, 400)
        except Exception as error:
            self.send_json({"error": str(error) or type(error).__name__}, 500)

    def upload(self, name, data):
        name = safe_name(name)
        if Path(name).suffix not in ALLOWED:
            return {"error": "Only image files (png, jpg, gif, bmp, webp) can be uploaded."}
        path = free_name(name)
        path.write_bytes(data)
        return {"name": path.name}

    def analyse(self, body):
        if Path(body["name"]).name not in image_names():
            return {"error": "Image not found in the images folder."}
        suspect = IMAGES / Path(body["name"]).name
        result = {"report": analyse(suspect)}
        if body.get("original"):
            result["comparison"] = compare_images(IMAGES / Path(body["original"]).name, suspect)
        return result

    def send_json(self, data, status=200):
        self.reply(status, "application/json", json.dumps(data).encode())

    def reply(self, status, kind, content):
        self.send_response(status)
        self.send_header("Content-Type", kind)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def log_message(self, *args):
        pass


def main():
    make_samples()
    url = f"http://localhost:{PORT}"
    print(f"Image forensics tool running at {url}")
    print(f"Images folder: {IMAGES}")
    print("Press Ctrl+C to stop.")
    webbrowser.open(url)
    try:
        HTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
