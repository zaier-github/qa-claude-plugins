#!/usr/bin/env python3
"""
capture_ui.py — Capture UI screenshots and CSS data using Playwright.
Usage: python scripts/capture_ui.py --url <URL> --output <output_dir> [--widths 1440 375]
"""
import argparse
import json
import os
import sys
import time

def capture(url: str, output_dir: str, widths: list[int]) -> None:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Playwright not installed. Run: pip install playwright && playwright install chromium --break-system-packages")
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        for width in widths:
            height = 900 if width >= 1024 else 812
            context = browser.new_context(viewport={"width": width, "height": height})
            page = context.new_page()

            print(f"  Navigating to {url} at {width}px...")
            page.goto(url, wait_until="networkidle", timeout=30000)
            time.sleep(1)  # Allow any JS animations to settle

            # Full-page screenshot
            full_path = os.path.join(output_dir, f"fullpage_{width}.png")
            page.screenshot(path=full_path, full_page=True)
            print(f"  Saved: {full_path}")

            # Viewport-only screenshot
            vp_path = os.path.join(output_dir, f"viewport_{width}.png")
            page.screenshot(path=vp_path, full_page=False)

            # Extract computed CSS for key interactive elements
            css_data = page.evaluate("""() => {
                const selectors = ['button', 'a', 'input', 'select', 'textarea', '[role="button"]'];
                const results = {};
                selectors.forEach(sel => {
                    const el = document.querySelector(sel);
                    if (el) {
                        const styles = window.getComputedStyle(el);
                        results[sel] = {
                            backgroundColor: styles.backgroundColor,
                            color: styles.color,
                            fontSize: styles.fontSize,
                            fontWeight: styles.fontWeight,
                            borderRadius: styles.borderRadius,
                            padding: styles.padding,
                            border: styles.border
                        };
                    }
                });
                return results;
            }""")

            css_path = os.path.join(output_dir, f"computed_css_{width}.json")
            with open(css_path, "w") as f:
                json.dump(css_data, f, indent=2)
            print(f"  Saved CSS data: {css_path}")

            # Check for early vs late load (simple CLS proxy)
            time.sleep(2)
            late_path = os.path.join(output_dir, f"late_load_{width}.png")
            page.screenshot(path=late_path, full_page=False)

            context.close()

        browser.close()
        print(f"\nCapture complete. Files saved to: {output_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Capture UI screenshots for audit")
    parser.add_argument("--url", required=True, help="URL to capture")
    parser.add_argument("--output", required=True, help="Output directory")
    parser.add_argument("--widths", nargs="+", type=int, default=[1440, 375],
                        help="Viewport widths to test (default: 1440 375)")
    args = parser.parse_args()

    capture(args.url, args.output, args.widths)