#!/usr/bin/env python3
"""
check_headers.py — Check a URL for security response headers.
Usage: python scripts/check_headers.py --url <URL>
"""
import argparse
import urllib.request
import urllib.error
import sys

SECURITY_HEADERS = [
    {
        "name": "Strict-Transport-Security",
        "alias": "HSTS",
        "required": True,
        "good_value_hint": "max-age=31536000; includeSubDomains",
        "description": "Forces HTTPS connections",
        "severity": "HIGH"
    },
    {
        "name": "Content-Security-Policy",
        "alias": "CSP",
        "required": True,
        "good_value_hint": "default-src 'self'; ...",
        "description": "Restricts resources the browser can load (prevents XSS)",
        "severity": "HIGH"
    },
    {
        "name": "X-Frame-Options",
        "alias": "XFO",
        "required": True,
        "good_value_hint": "DENY or SAMEORIGIN",
        "description": "Prevents clickjacking by disabling iframe embedding",
        "severity": "MEDIUM"
    },
    {
        "name": "X-Content-Type-Options",
        "alias": "XCTO",
        "required": True,
        "good_value_hint": "nosniff",
        "description": "Prevents MIME type sniffing",
        "severity": "MEDIUM"
    },
    {
        "name": "Referrer-Policy",
        "alias": "RP",
        "required": True,
        "good_value_hint": "strict-origin-when-cross-origin or no-referrer",
        "description": "Controls how much referrer info is sent",
        "severity": "LOW"
    },
    {
        "name": "Permissions-Policy",
        "alias": "PP",
        "required": False,
        "good_value_hint": "camera=(), microphone=(), geolocation=()",
        "description": "Restricts browser feature access",
        "severity": "LOW"
    },
    {
        "name": "X-XSS-Protection",
        "alias": "XXP",
        "required": False,
        "good_value_hint": "Should be absent (deprecated) or 0",
        "description": "Legacy XSS filter — modern browsers ignore it; CSP is the replacement",
        "severity": "INFO"
    },
    {
        "name": "Cache-Control",
        "alias": "CC",
        "required": False,
        "good_value_hint": "no-store for sensitive pages",
        "description": "Check that sensitive pages aren't cached by proxies",
        "severity": "LOW"
    },
]

SEVERITY_ICONS = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢", "INFO": "ℹ️"}


def check(url: str) -> None:
    print(f"Checking security headers for: {url}\n")

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (security-header-checker)"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            headers = {k.lower(): v for k, v in resp.getheaders()}
            effective_url = resp.geturl()
            status = resp.status
    except urllib.error.HTTPError as e:
        headers = {k.lower(): v for k, v in e.headers.items()}
        effective_url = url
        status = e.code
    except Exception as e:
        print(f"Error fetching URL: {e}")
        sys.exit(1)

    print(f"HTTP Status: {status}")
    if effective_url != url:
        print(f"Redirected to: {effective_url}")
    print()

    missing_required = []
    present_headers = []

    for h in SECURITY_HEADERS:
        header_lower = h["name"].lower()
        value = headers.get(header_lower)
        icon = SEVERITY_ICONS.get(h["severity"], "⚪")

        if value:
            present_headers.append((h, value))
            print(f"  ✅ {h['name']}")
            print(f"     Value: {value}")
        else:
            if h["required"]:
                missing_required.append(h)
                print(f"  {icon} MISSING: {h['name']} [{h['severity']}]")
                print(f"     {h['description']}")
                print(f"     Recommended: {h['good_value_hint']}")
            else:
                print(f"  ⚠️  OPTIONAL/MISSING: {h['name']}")
                print(f"     {h['description']}")
        print()

    # Summary
    print("=" * 50)
    print(f"SUMMARY: {len(present_headers)}/{len(SECURITY_HEADERS)} headers present")
    if missing_required:
        print(f"\nMissing required headers ({len(missing_required)}):")
        for h in missing_required:
            icon = SEVERITY_ICONS.get(h["severity"], "⚪")
            print(f"  {icon} {h['name']} ({h['severity']})")
    else:
        print("✅ All required security headers present!")

    # Check for HTTP (no HTTPS)
    if effective_url.startswith("http://"):
        print("\n🔴 CRITICAL: Site is served over HTTP, not HTTPS!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check security response headers")
    parser.add_argument("--url", required=True, help="URL to check")
    args = parser.parse_args()
    check(args.url)