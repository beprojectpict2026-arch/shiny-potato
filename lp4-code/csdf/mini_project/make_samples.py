"""CSDF Mini-project - creates the tampered demo images in the images/ folder.

Starting from the clean photo images/original.png it makes stego.png (a secret message hidden in the
pixel bits) and appended.png (a password hidden after the end of the image). edited.jpg is a ready-made
photo with a Photoshop trace and a hidden program. Libs used (standard library only): pathlib, forensics.py.
"""

from pathlib import Path

from forensics import build_png, decode_pixels, parse_png

IMAGES = Path(__file__).parent / "images"
SECRET = b"MEET AT 9PM\x00"


def make_samples(folder=IMAGES):
    original = folder / "original.png"
    if not original.exists():
        print("Put a clean photo at", original, "and run this again.")
        return
    data = original.read_bytes()
    _, info, text, _ = parse_png(data)
    rgb = decode_pixels(data)

    bits = [(byte >> (7 - i)) & 1 for byte in SECRET for i in range(8)]
    stego = bytearray(rgb)
    for i, bit in enumerate(bits):
        stego[i] = (stego[i] & 0xFE) | bit

    files = {
        "stego.png": build_png(info["width"], info["height"], bytes(stego), text),
        "appended.png": data + b"<<payload: password=hunter2>>",
    }
    for name, content in files.items():
        if not (folder / name).exists():
            (folder / name).write_bytes(content)
            print("created", folder / name)


if __name__ == "__main__":
    make_samples()
