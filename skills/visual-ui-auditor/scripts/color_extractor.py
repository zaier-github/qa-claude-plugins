#!/usr/bin/env python3
"""
color_extractor.py — Extract dominant colors from a screenshot and report hex values.
Usage: python scripts/color_extractor.py --image <path> [--top 10]
"""
import argparse
import sys
from collections import Counter


def rgb_to_hex(r: int, g: int, b: int) -> str:
    return f"#{r:02x}{g:02x}{b:02x}"


def quantize_channel(v: int, bucket: int = 16) -> int:
    """Bucket channel value to reduce noise."""
    return (v // bucket) * bucket


def extract_colors(image_path: str, top_n: int = 10) -> list[dict]:
    try:
        from PIL import Image
    except ImportError:
        print("Pillow not installed. Run: pip install Pillow --break-system-packages")
        sys.exit(1)

    img = Image.open(image_path).convert("RGB")
    # Resize for performance
    img = img.resize((200, 200))

    pixels = list(img.getdata())
    # Quantize to reduce noise
    quantized = [(quantize_channel(r), quantize_channel(g), quantize_channel(b))
                 for r, g, b in pixels]

    counter = Counter(quantized)
    total = len(quantized)

    results = []
    for (r, g, b), count in counter.most_common(top_n):
        results.append({
            "hex": rgb_to_hex(r, g, b),
            "rgb": f"rgb({r}, {g}, {b})",
            "percentage": round((count / total) * 100, 1)
        })
    return results


def main():
    parser = argparse.ArgumentParser(description="Extract dominant colors from screenshot")
    parser.add_argument("--image", required=True, help="Path to image file")
    parser.add_argument("--top", type=int, default=10, help="Number of top colors to show")
    args = parser.parse_args()

    print(f"Analyzing: {args.image}")
    colors = extract_colors(args.image, args.top)

    print(f"\nTop {args.top} dominant colors:")
    print(f"{'Hex':<12} {'RGB':<22} {'Coverage'}")
    print("-" * 40)
    for c in colors:
        print(f"{c['hex']:<12} {c['rgb']:<22} {c['percentage']}%")


if __name__ == "__main__":
    main()