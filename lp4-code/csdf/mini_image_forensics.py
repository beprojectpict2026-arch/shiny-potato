"""CSDF Mini-project - Digital forensic tool for images.

Problem statement: examine an image file for evidence of tampering - identify the
real file type, compute integrity hashes, extract metadata (PNG text chunks / JPEG
EXIF), detect editing software traces, find data hidden after the end-of-image
marker, extract messages hidden in pixel least-significant bits (LSB steganography)
and compare a suspect image with the original at pixel level.

New libs used (all standard library, no Pillow): hashlib, struct, zlib (PNG
decode/encode), random, tempfile, pathlib.

Driver: builds an original PNG, three tampered variants (LSB-stego, appended payload,
edited-with-Photoshop JPEG) in a temp folder, analyses each and compares to the
original. No input is taken at runtime.
"""

import hashlib
import random
import struct
import tempfile
import zlib
from pathlib import Path

PNG_SIG = b"\x89PNG\r\n\x1a\n"
EDITORS = ("photoshop", "gimp", "lightroom", "paint.net", "pixlr", "snapseed")


# ----------------------------- PNG helpers ----------------------------------
def png_chunk(kind, data):
    body = kind + data
    return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body))


def build_png(width, height, rgb, text=None):
    """Encode raw RGB bytes as PNG; `text` is a dict of tEXt metadata."""
    rows = b"".join(b"\x00" + rgb[y * width * 3:(y + 1) * width * 3] for y in range(height))
    out = PNG_SIG + png_chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
    for key, value in (text or {}).items():
        out += png_chunk(b"tEXt", key.encode() + b"\x00" + value.encode())
    return out + png_chunk(b"IDAT", zlib.compress(rows)) + png_chunk(b"IEND", b"")


def parse_png(data):
    """Return (chunks, info, text, trailing_bytes). chunks = [(type, data)]."""
    pos, chunks = 8, []
    while pos < len(data):
        length, kind = struct.unpack(">I4s", data[pos:pos + 8])
        body = data[pos + 8:pos + 8 + length]
        chunks.append((kind, body))
        pos += 12 + length
        if kind == b"IEND":
            break
    width, height, depth, ctype = struct.unpack(">IIBB", chunks[0][1][:10])
    text = {}
    for kind, body in chunks:
        if kind == b"tEXt":
            key, _, value = body.partition(b"\x00")
            text[key.decode()] = value.decode(errors="replace")
    info = {"width": width, "height": height, "depth": depth, "color_type": ctype}
    return chunks, info, text, data[pos:]


def decode_pixels(data):
    """Decode an 8-bit non-interlaced PNG into raw bytes (handles all filters)."""
    chunks, info, _, _ = parse_png(data)
    bpp = {0: 1, 2: 3, 6: 4}[info["color_type"]]
    stride = info["width"] * bpp
    raw = zlib.decompress(b"".join(body for kind, body in chunks if kind == b"IDAT"))
    out, prev = bytearray(), bytearray(stride)
    for y in range(info["height"]):
        ftype, line = raw[y * (stride + 1)], bytearray(raw[y * (stride + 1) + 1:(y + 1) * (stride + 1)])
        for i in range(stride):
            a = line[i - bpp] if i >= bpp else 0
            b = prev[i]
            c = prev[i - bpp] if i >= bpp else 0
            if ftype == 1:
                line[i] = (line[i] + a) & 255
            elif ftype == 2:
                line[i] = (line[i] + b) & 255
            elif ftype == 3:
                line[i] = (line[i] + (a + b) // 2) & 255
            elif ftype == 4:
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                line[i] = (line[i] + (a if pa <= pb and pa <= pc else b if pb <= pc else c)) & 255
        out += line
        prev = line
    return bytes(out)


# ----------------------------- JPEG helpers ---------------------------------
def build_jpeg(exif):
    """Build a tiny structurally valid JPEG (segments only) with EXIF tags."""
    entries, blob = b"", b""
    data_start = 8 + 2 + 12 * len(exif) + 4
    for tag, value in exif.items():
        raw = value.encode() + b"\x00"
        entries += struct.pack("<HHII", tag, 2, len(raw), data_start + len(blob))
        blob += raw
    tiff = b"II*\x00" + struct.pack("<I", 8) + struct.pack("<H", len(exif)) + entries + b"\x00" * 4 + blob
    app1 = b"Exif\x00\x00" + tiff
    sos = b"\xff\xda" + struct.pack(">H", 8) + b"\x01\x01\x00\x00\x3f\x00"
    return b"\xff\xd8\xff\xe1" + struct.pack(">H", len(app1) + 2) + app1 + sos + b"\x12\x34\x56" + b"\xff\xd9"


def parse_jpeg(data):
    """Return (exif_dict, trailing_bytes) by walking the JPEG segments."""
    names = {0x010F: "Make", 0x0110: "Model", 0x0131: "Software", 0x0132: "DateTime"}
    pos, exif = 2, {}
    while pos < len(data):
        marker = data[pos + 1]
        length = struct.unpack(">H", data[pos + 2:pos + 4])[0]
        seg = data[pos + 4:pos + 2 + length]
        if marker == 0xE1 and seg.startswith(b"Exif\x00\x00"):
            tiff = seg[6:]
            endian = "<" if tiff[:2] == b"II" else ">"
            ifd = struct.unpack(endian + "I", tiff[4:8])[0]
            count = struct.unpack(endian + "H", tiff[ifd:ifd + 2])[0]
            for i in range(count):
                tag, kind, n, off = struct.unpack(endian + "HHII", tiff[ifd + 2 + 12 * i:ifd + 14 + 12 * i])
                if kind == 2 and tag in names:
                    exif[names[tag]] = tiff[off:off + n].rstrip(b"\x00").decode(errors="replace")
        if marker == 0xDA:  # start of scan: entropy data follows, find EOI
            eoi = data.find(b"\xff\xd9", pos + 2 + length)
            return exif, data[eoi + 2:]
        pos += 2 + length
    return exif, b""


# ----------------------------- Analysis -------------------------------------
def extract_lsb_message(pixels, limit=200):
    """Read LSBs of the pixel bytes; return text if it forms a printable message."""
    chars = bytearray()
    for i in range(0, min(len(pixels), limit * 8), 8):
        byte = 0
        for bit in pixels[i:i + 8]:
            byte = (byte << 1) | (bit & 1)
        if byte == 0:
            break
        chars.append(byte)
    text = chars.decode("latin-1")
    return text if len(text) >= 4 and all(32 <= ord(c) < 127 for c in text) else None


def analyse(path):
    data = Path(path).read_bytes()
    report = {"file": Path(path).name, "size": len(data), "findings": []}
    report["sha256"] = hashlib.sha256(data).hexdigest()
    report["md5"] = hashlib.md5(data).hexdigest()
    findings = report["findings"]

    if data.startswith(PNG_SIG):
        _, info, meta, trailing = parse_png(data)
        report.update(type="PNG", info=info, metadata=meta)
        message = extract_lsb_message(decode_pixels(data))
        if message:
            findings.append(f"Hidden LSB message in pixels: {message!r}")
    elif data.startswith(b"\xff\xd8"):
        meta, trailing = parse_jpeg(data)
        report.update(type="JPEG", info={}, metadata=meta)
        if not meta:
            findings.append("No EXIF metadata (possibly stripped)")
    else:
        report.update(type="UNKNOWN", info={}, metadata={})
        findings.append("Unrecognised file signature: extension may be spoofed")
        trailing = b""

    if trailing:
        findings.append(f"{len(trailing)} bytes of data after end-of-image marker: {trailing[:30]!r}")
    software = report["metadata"].get("Software", "").lower()
    if any(editor in software for editor in EDITORS):
        findings.append(f"Edited with image software: {report['metadata']['Software']}")
    return report


def compare(original, suspect):
    """Hash and pixel-level comparison of two PNG files."""
    a, b = Path(original).read_bytes(), Path(suspect).read_bytes()
    result = {"identical_hash": hashlib.sha256(a).digest() == hashlib.sha256(b).digest()}
    pa, pb = decode_pixels(a), decode_pixels(b)
    diffs = [abs(x - y) for x, y in zip(pa, pb) if x != y]
    result["changed_values"] = len(diffs)
    result["max_difference"] = max(diffs, default=0)
    return result


def print_report(r):
    print(f"--- {r['file']} ({r['type']}, {r['size']} bytes)")
    print(f"    sha256: {r['sha256'][:32]}...  md5: {r['md5']}")
    if r["info"]:
        print(f"    image : {r['info']['width']}x{r['info']['height']}")
    print(f"    meta  : {r['metadata'] or 'none'}")
    print("    verdict:", "SUSPICIOUS" if r["findings"] else "no anomalies found")
    for f in r["findings"]:
        print("      *", f)


# ----------------------------- Driver ---------------------------------------
def make_samples(folder):
    """Create the original image plus three tampered variants."""
    rng = random.Random(7)
    w = h = 48
    rgb = bytes(min(255, (x * 4 + y * 2 + rng.randrange(8))) for y in range(h) for x in range(w) for _ in range(3))
    meta = {"Software": "Canon DIGIC", "Comment": "holiday photo"}
    original = build_png(w, h, rgb, meta)

    secret = b"MEET AT 9PM\x00"
    bits = [(byte >> (7 - i)) & 1 for byte in secret for i in range(8)]
    stego = bytearray(rgb)
    for i, bit in enumerate(bits):
        stego[i] = (stego[i] & 0xFE) | bit

    files = {
        "original.png": original,
        "stego.png": build_png(w, h, bytes(stego), meta),
        "appended.png": original + b"<<payload: password=hunter2>>",
        "edited.jpg": build_jpeg({0x010F: "Canon", 0x0110: "EOS 80D", 0x0131: "Adobe Photoshop 25.0",
                                  0x0132: "2026:10:14 10:00:00"}) + b"MZ\x90\x00hidden-exe",
    }
    for name, content in files.items():
        (folder / name).write_bytes(content)


def main():
    with tempfile.TemporaryDirectory() as tmp:
        folder = Path(tmp)
        make_samples(folder)
        print("=== Image analysis ===")
        for name in ("original.png", "stego.png", "appended.png", "edited.jpg"):
            print_report(analyse(folder / name))
        print("\n=== Pixel comparison with original.png ===")
        for name in ("stego.png", "appended.png"):
            print(name, "->", compare(folder / "original.png", folder / name))


if __name__ == "__main__":
    main()
