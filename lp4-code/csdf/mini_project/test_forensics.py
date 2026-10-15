"""CSDF Mini-project - pytest tests for the image forensics tool.

Test your own image: set image_path below (a file inside images/, or a full path) and run
`pytest -s test_forensics.py` to see its report. The other tests check the four demo images.
Libs used: pytest, plus forensics.py and make_samples.py.
"""

import struct
from pathlib import Path

import pytest

from forensics import analyse, compare_images, print_report
from make_samples import SECRET, make_samples
from web_app import safe_name

FOLDER = Path(__file__).parent

image_path = "images/stego.png"
original_path = "images/original.png"


@pytest.fixture(scope="session", autouse=True)
def demo_images():
    make_samples()


def test_your_image():
    path = FOLDER / image_path
    assert path.exists(), f"Image not found: {path}"
    report = analyse(path)
    print()
    print_report(report)
    if original_path and path.name != Path(original_path).name:
        print("    compared with", original_path, "->", compare_images(FOLDER / original_path, path))
    assert report["type"] in ("PNG", "JPEG", "UNKNOWN")


def test_original_is_clean():
    report = analyse(FOLDER / "images/original.png")
    assert report["findings"] == []


def test_hidden_message_found():
    report = analyse(FOLDER / "images/stego.png")
    assert any("MEET AT 9PM" in finding for finding in report["findings"])


def test_appended_data_found():
    report = analyse(FOLDER / "images/appended.png")
    assert any("after end-of-image" in finding for finding in report["findings"])


def test_editing_software_found():
    report = analyse(FOLDER / "images/edited.jpg")
    assert any("Photoshop" in finding for finding in report["findings"])
    assert any("after end-of-image" in finding for finding in report["findings"])


def test_pixel_comparison():
    result = compare_images(FOLDER / "images/original.png", FOLDER / "images/stego.png")
    assert 0 < result["changed_values"] <= len(SECRET) * 8
    assert result["max_difference"] == 1


def test_different_formats_cannot_be_compared():
    result = compare_images(FOLDER / "images/original.png", FOLDER / "images/edited.jpg")
    assert "error" in result


def make_jpeg(width, height):
    sof = b"\xff\xc0" + struct.pack(">HBHHB", 11, 8, height, width, 1) + b"\x01\x11\x00"
    sos = b"\xff\xda" + struct.pack(">H", 8) + b"\x01\x01\x00\x00\x3f\x00"
    return b"\xff\xd8" + sof + sos + b"\x12\x34\x56" + b"\xff\xd9"


def test_jpeg_dimensions(tmp_path):
    (tmp_path / "a.jpg").write_bytes(make_jpeg(50, 30))
    report = analyse(tmp_path / "a.jpg")
    assert report["info"] == {"width": 50, "height": 30}


def test_second_jpeg_appended_is_flagged(tmp_path):
    (tmp_path / "a.jpg").write_bytes(make_jpeg(50, 30) + make_jpeg(5, 5))
    report = analyse(tmp_path / "a.jpg")
    assert any("after end-of-image" in finding for finding in report["findings"])


def test_safe_name():
    assert safe_name("my photo (1).JPG") == "my_photo_1.jpg"
    assert safe_name("../../evil.png") == "evil.png"
    assert safe_name("C:\\Users\\me\\pic?.png") == "pic.png"
    assert safe_name("???.png") == "image.png"
