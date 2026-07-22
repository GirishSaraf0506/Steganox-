"""Image I/O and format detection utilities."""

import os

from PIL import Image


def get_image_capacity(image_path: str) -> int:
    """Return max bytes that can be hidden in the image (LSB method)."""
    img = Image.open(image_path).convert("RGB")
    w, h = img.size
    return (w * h * 3) // 8


def get_image_info(image_path: str) -> dict:
    """Return basic image metadata."""
    img = Image.open(image_path)
    size_kb = os.path.getsize(image_path) / 1024
    return {
        "format": img.format,
        "mode": img.mode,
        "width": img.size[0],
        "height": img.size[1],
        "size_kb": round(size_kb, 2),
        "capacity_bytes": get_image_capacity(image_path),
    }


def convert_to_png(image_path: str, output_path: str) -> str:
    """Convert any supported image to PNG (lossless, recommended for steganography)."""
    img = Image.open(image_path).convert("RGB")
    img.save(output_path, format="PNG")
    return output_path
