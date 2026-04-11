#!/usr/bin/env python3
"""
axe_scan.py — Run axe-core accessibility scan via Playwright.
Usage: python scripts/axe_scan.py --url <URL> --output <output_dir> [--level aa]

Requires: pip install playwright --break-system-packages && playwright install chromium
The axe-core library is loaded from CDN at runtime.
"""
import argparse
import json
import os
import sys
from datetime import datetime


AXE_CDN = "https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.9.1/axe.min.js"

IMPACT_ORDER = {"critical": 0, "serious": 1, "moderate": 2, "minor": 3}


def run_scan(url: str, output_dir: str, level: str = "aa") -> dict:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Playwright not installed. Run: pip install playwright --break-system-packages && playwright install chromium")
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print(f"Loading: {url}")
        page.goto(url, wait_until="networkidle", timeout=30000)

        # Inject axe-core from CDN
        page.add_script_tag(url=AXE_CDN)
        page.wait_for_function("typeof axe !== 'undefined'")

        # Run axe with configured standard
        tags = ["wcag2a", "wcag2aa", "wcag21aa", "wcag22aa", "best-practice"] if level == "aa" else ["wcag2a"]
        print(f"Running axe-core (WCAG {level.upper()})...")

        results = page.evaluate(f"""async () => {{
            return await axe.run(document, {{
                runOnly: {{ type: 'tag', values: {json.dumps(tags)} }}
            }});
        }}""")

        browser.close()

    return results


def format_report(results: dict, url: str) -> str:
    violations = results.get("violations", [])
    passes = len(results.get("passes", []))
    incomplete = len(results.get("incomplete", []))

    violations.sort(key=lambda v: IMPACT_ORDER.get(v.get("impact", "minor"), 99))

    lines = [
        f"# Accessibility Audit Report",
        f"",
        f"**URL**: {url}",
        f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"**Tool**: axe-core 4.9.1",
        f"",
        f"## Summary",
        f"",
        f"| Metric | Count |",
        f"|--------|-------|",
        f"| ✅ Passes | {passes} |",
        f"| ❌ Violations | {len(violations)} |",
        f"| ⚠️ Needs review | {incomplete} |",
        f"",
    ]

    if not violations:
        lines.append("🎉 **No violations found by automated scan.** Complete manual checklist to verify remaining issues.")
        return "\n".join(lines)

    lines.append("## Violations\n")

    impact_icons = {"critical": "🔴", "serious": "🟠", "moderate": "🟡", "minor": "🟢"}

    for v in violations:
        icon = impact_icons.get(v.get("impact", "minor"), "⚪")
        lines.append(f"### {icon} [{v.get('impact', '').upper()}] {v['description']}")
        lines.append(f"")
        lines.append(f"- **Rule ID**: `{v['id']}`")
        lines.append(f"- **WCAG**: {', '.join(v.get('tags', []))}")
        lines.append(f"- **Help**: {v.get('helpUrl', '')}")
        lines.append(f"")

        nodes = v.get("nodes", [])[:3]  # Show up to 3 affected elements
        if nodes:
            lines.append(f"**Affected elements** ({len(v['nodes'])} total, showing first {len(nodes)}):")
            for node in nodes:
                target = node.get("target", ["(unknown)"])
                lines.append(f"  - `{target[0]}`")
                for check in node.get("any", []) + node.get("all", []) + node.get("none", []):
                    if check.get("message"):
                        lines.append(f"    - {check['message']}")
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Run axe-core accessibility scan")
    parser.add_argument("--url", required=True, help="URL to scan")
    parser.add_argument("--output", required=True, help="Output directory")
    parser.add_argument("--level", default="aa", choices=["a", "aa"], help="WCAG level (default: aa)")
    args = parser.parse_args()

    results = run_scan(args.url, args.output, args.level)

    # Save raw results
    raw_path = os.path.join(args.output, "axe_results.json")
    with open(raw_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Raw results: {raw_path}")

    # Save formatted report
    report = format_report(results, args.url)
    report_path = os.path.join(args.output, "axe_report.md")
    with open(report_path, "w") as f:
        f.write(report)
    print(f"Report: {report_path}")

    violations = results.get("violations", [])
    print(f"\n{'='*40}")
    print(f"Violations found: {len(violations)}")
    for v in violations:
        print(f"  [{v.get('impact','?').upper()}] {v['id']}: {len(v['nodes'])} element(s)")


if __name__ == "__main__":
    main()