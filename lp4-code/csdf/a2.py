"""CSDF Assignment 2 - Generate and verify a CAPTCHA image.

Problem statement: create a CAPTCHA image containing random characters (with
noise lines, dots and per-character jitter) and verify a user's answer against
the stored text, with single-use tokens and a limited number of attempts.

New libs used (all standard library): random, secrets, zlib + struct (to write
the PNG without Pillow), hashlib (answers are stored hashed).

Driver: generates a CAPTCHA with a fixed seed, saves it as captcha_sample.png
next to this file, then verifies a correct answer, a wrong answer and a replay.
No input is taken at runtime.
"""

import hashlib
import random
import secrets
import struct
import zlib
from pathlib import Path

# 5x7 bitmap font for the characters we use (no look-alikes such as 0/O, 1/I).
FONT = {
    "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    "B": ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
    "C": ["01110", "10001", "10000", "10000", "10000", "10001", "01110"],
    "D": ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
    "E": ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    "F": ["11111", "10000", "10000", "11110", "10000", "10000", "10000"],
    "H": ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
    "K": ["10001", "10010", "10100", "11000", "10100", "10010", "10001"],
    "M": ["10001", "11011", "10101", "10101", "10001", "10001", "10001"],
    "N": ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
    "P": ["11110", "10001", "10001", "11110", "10000", "10000", "10000"],
    "R": ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    "T": ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    "X": ["10001", "10001", "01010", "00100", "01010", "10001", "10001"],
    "2": ["01110", "10001", "00001", "00110", "01000", "10000", "11111"],
    "3": ["11110", "00001", "00001", "01110", "00001", "00001", "11110"],
    "4": ["00010", "00110", "01010", "10010", "11111", "00010", "00010"],
    "5": ["11111", "10000", "11110", "00001", "00001", "10001", "01110"],
    "7": ["11111", "00001", "00010", "00100", "01000", "01000", "01000"],
    "9": ["01110", "10001", "10001", "01111", "00001", "00010", "01100"],
}
SCALE, WIDTH, HEIGHT = 5, 200, 70


def draw_captcha(text, rng):
    """Return a WIDTH x HEIGHT grid of grey levels (0 = black, 255 = white)."""
    img = [[255] * WIDTH for _ in range(HEIGHT)]
    x = 15
    for ch in text:
        y0 = 17 + rng.randint(-6, 6)  # vertical jitter per character
        for r, row in enumerate(FONT[ch]):
            for c, bit in enumerate(row):
                if bit == "1":
                    for dy in range(SCALE):
                        for dx in range(SCALE):
                            img[y0 + r * SCALE + dy][x + c * SCALE + dx] = 30
        x += 5 * SCALE + 8
    for _ in range(5):  # noise lines
        x1, y1, x2, y2 = rng.randrange(WIDTH), rng.randrange(HEIGHT), rng.randrange(WIDTH), rng.randrange(HEIGHT)
        for i in range(101):
            px, py = x1 + (x2 - x1) * i // 100, y1 + (y2 - y1) * i // 100
            img[py][px] = 140
    for _ in range(250):  # noise dots
        img[rng.randrange(HEIGHT)][rng.randrange(WIDTH)] = rng.choice((0, 120, 200))
    return img


def save_png(img, path):
    """Write a greyscale 8-bit PNG using only zlib and struct."""
    raw = b"".join(b"\x00" + bytes(row) for row in img)

    def chunk(kind, data):
        body = kind + data
        return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body))

    header = struct.pack(">IIBBBBB", WIDTH, HEIGHT, 8, 0, 0, 0, 0)
    Path(path).write_bytes(
        b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header) + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b"")
    )


class CaptchaService:
    """Issues CAPTCHAs and verifies answers (case-insensitive, single use)."""

    MAX_ATTEMPTS = 3

    def __init__(self, seed=None):
        self.rng = random.Random(seed)
        self.store = {}  # token -> [sha256(answer), attempts_left]

    @staticmethod
    def _hash(text):
        return hashlib.sha256(text.upper().encode()).hexdigest()

    def generate(self, path, length=5):
        text = "".join(self.rng.choice(list(FONT)) for _ in range(length))
        token = secrets.token_hex(8)
        self.store[token] = [self._hash(text), self.MAX_ATTEMPTS]
        save_png(draw_captcha(text, self.rng), path)
        return token, text  # text is returned only so the driver can demo it

    def verify(self, token, answer):
        entry = self.store.get(token)
        if entry is None:
            return False  # unknown or already used
        if self._hash(answer.strip()) == entry[0]:
            del self.store[token]  # single use: prevents replay
            return True
        entry[1] -= 1
        if entry[1] == 0:
            del self.store[token]
        return False


def main():
    service = CaptchaService(seed=42)
    out = Path(__file__).with_name("captcha_sample.png")
    token, text = service.generate(out)
    print(f"CAPTCHA image saved to {out.name} ({out.stat().st_size} bytes), hidden text: {text}")
    print("Wrong answer 'ZZZZZ'  ->", service.verify(token, "ZZZZZ"))
    print(f"Correct answer '{text.lower()}' ->", service.verify(token, text.lower()))
    print("Replay of same token  ->", service.verify(token, text))


if __name__ == "__main__":
    main()
