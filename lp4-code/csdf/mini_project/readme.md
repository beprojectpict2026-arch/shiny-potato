# Image Forensics Tool (CSDF mini-project)

A small tool that looks **inside** an image file, not at the picture, to find signs of tampering or hidden data.
It has a web page and a pytest file, and it uses only the Python standard library.

## The demo images (`images/`, all 720 x 753)

All four are made from one photo of Mumbai harbour. Open them in any photo viewer and they look the same. That is the point: the tampering cannot be seen by eye, so a forensic tool is needed.

| Image | What was done to it | What the tool shows |
|---|---|---|
| `original.png` | Nothing. This is the clean reference. | No anomalies found |
| `stego.png` | A secret message (`MEET AT 9PM`) is hidden in the pixel data (steganography). | SUSPICIOUS: hidden LSB message found |
| `appended.png` | A password is added to the end of the file, after the image data. | SUSPICIOUS: bytes found after the end-of-image marker |
| `edited.jpg` | Made to look edited in Photoshop, with a program hidden after the image end. | SUSPICIOUS: editing software and extra bytes found |

### What each one means

- **stego (steganography):** every pixel colour is a number from 0 to 255. Changing the last bit (the "least significant bit", LSB) changes the number by at most 1, which nobody can see. The message is written bit by bit into those last bits. The tool reads them back and shows the message. Compared with `original.png`, only 48 values differ, each by 1.
- **appended:** an image file has an end marker, and viewers stop reading there. Anything added after it is ignored by viewers but still stored in the file. The pixels are identical to the original (0 changes), but the file hash is different, which proves the file was changed.
- **edited:** photos store hidden details called metadata (EXIF), such as the camera model and the software that last saved the file. Here the Software field says `Adobe Photoshop 25.0`. This was added for the demo, the photo was not really opened in Photoshop. Metadata is easy to fake, so it is a clue, not proof. The 14 bytes after the image end start with `MZ`, the signature of a Windows program.

## What the tool checks

1. **Real file type:** read from the first bytes of the file (the file signature), not from the name. A text file renamed to `.png` is reported as UNKNOWN: extension may be spoofed.
2. **Hashes (SHA-256 and MD5):** a fingerprint of the file. Change one byte and the hash changes.
3. **Metadata:** PNG text chunks and JPEG EXIF, including editing-software traces.
4. **Data after the image ends:** anything past the end-of-image marker.
5. **LSB steganography:** hidden text in the pixel bits (PNG only).
6. **Original vs suspect:** pixel-by-pixel comparison of two PNGs of the same size.

## Run it

```
cd lp4-code
uv run python csdf/mini_project/web_app.py     # web page at http://localhost:8000, Ctrl+C to stop
uv run pytest csdf/mini_project -s             # tests, prints the report for image_path
```

- **Web page:** click an image (or upload one, it is saved in `images/`), optionally choose an original to compare with, then click Analyse.
- **Your own image in pytest:** set `image_path` at the top of `test_forensics.py` and run the command above.
- **Spoofed extension test:** save a text file, rename it to `secret.png`, put it in `images/` and analyse it.

## Files

| File | Purpose |
|---|---|
| `forensics.py` | The analysis code (PNG and JPEG parsing, hashes, LSB, comparison) |
| `web_app.py`, `index.html` | The web page and the small local server behind it |
| `test_forensics.py` | pytest tests, plus the `image_path` test for your own image |
| `make_samples.py` | Builds `stego.png` and `appended.png` from `original.png` if they are missing |
| `images/` | Demo images and anything uploaded from the web page |

## Limits

- Pixel checks (hidden message, comparison) work on ordinary 8-bit PNG files only. JPEGs get the file type, hash, metadata and extra-data checks.
- The LSB check looks for a plain text message at the start of the pixel data. A message hidden some other way will not be found.
- A JPEG with no EXIF data (screenshots, images saved from websites) is flagged as possibly stripped. That alone does not mean it was tampered with.
