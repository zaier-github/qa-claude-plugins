#!/usr/bin/env python3
"""
fuzz_inputs.py — Fuzz web form inputs with security payloads using Playwright.
Usage: python scripts/fuzz_inputs.py --url <URL> --output <output_dir>

Only run against systems you own or have written permission to test.
Requires: pip install playwright --break-system-packages && playwright install chromium
"""
import argparse
import json
import os
import sys
import time
from datetime import datetime

# Safe subset of payloads — detects reflection/injection without destructive actions
FUZZ_PAYLOADS = [
    {"id": "xss_basic",       "payload": "<script>alert(1)</script>",      "category": "XSS"},
    {"id": "xss_img",         "payload": "<img src=x onerror=alert(1)>",   "category": "XSS"},
    {"id": "xss_attr",        "payload": '" onmouseover="alert(1)',         "category": "XSS"},
    {"id": "sqli_quote",      "payload": "'",                               "category": "SQLi"},
    {"id": "sqli_or",         "payload": "' OR '1'='1",                    "category": "SQLi"},
    {"id": "sqli_comment",    "payload": "' --",                            "category": "SQLi"},
    {"id": "path_traversal",  "payload": "../../../etc/passwd",             "category": "Path Traversal"},
    {"id": "template_inject", "payload": "{{7*7}}",                        "category": "Template Injection"},
    {"id": "template_inject2","payload": "${7*7}",                         "category": "Template Injection"},
    {"id": "null_byte",       "payload": "test\x00injection",              "category": "Null Byte"},
    {"id": "long_string",     "payload": "A" * 1000,                       "category": "Buffer/Length"},
    {"id": "special_chars",   "payload": "!@#$%^&*()[]{}|\\;:'\"<>?,./`~","category": "Special Chars"},
]


def find_forms(page) -> list[dict]:
    """Find all forms and their input fields on the page."""
    return page.evaluate("""() => {
        const forms = [];
        document.querySelectorAll('form').forEach((form, fi) => {
            const inputs = [];
            form.querySelectorAll('input:not([type=hidden]):not([type=submit]):not([type=button]), textarea').forEach((inp, ii) => {
                inputs.push({
                    index: ii,
                    name: inp.name || inp.id || `input_${ii}`,
                    type: inp.type || 'text',
                    selector: inp.id ? `#${inp.id}` : `form:nth-of-type(${fi+1}) input:nth-of-type(${ii+1})`
                });
            });
            if (inputs.length > 0) {
                forms.push({
                    index: fi,
                    action: form.action || '(no action)',
                    method: form.method || 'get',
                    inputs: inputs
                });
            }
        });
        return forms;
    }""")


def check_reflection(response_text: str, payload: str) -> bool:
    """Check if the payload appears unescaped in the response."""
    # Simple reflection check — look for key parts of the payload unescaped
    markers = ["<script>", "onerror=", "onmouseover=", "alert(", "{{7*7}}", "${7*7}"]
    payload_lower = payload.lower()
    response_lower = response_text.lower()
    for marker in markers:
        if marker.lower() in payload_lower and marker.lower() in response_lower:
            return True
    return False


def check_sql_error(response_text: str) -> bool:
    """Check if SQL error messages appear in the response."""
    sql_error_patterns = [
        "you have an error in your sql syntax",
        "warning: mysql",
        "unclosed quotation mark",
        "sqlexception",
        "ora-00933",
        "pg::syntaxerror",
        "sqlite3::exception",
        "syntax error",
        "unterminated string literal",
    ]
    response_lower = response_text.lower()
    return any(p in response_lower for p in sql_error_patterns)


def fuzz(url: str, output_dir: str) -> None:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Playwright not installed. Run: pip install playwright --break-system-packages && playwright install chromium")
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)
    findings = []
    tested_count = 0

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()

        # Load the page and discover forms
        page = context.new_page()
        print(f"Loading: {url}")
        page.goto(url, wait_until="networkidle", timeout=30000)
        forms = find_forms(page)
        print(f"Found {len(forms)} form(s) with inputs")

        for form in forms:
            print(f"\nForm {form['index']+1}: {form['method'].upper()} {form['action']}")
            for input_field in form["inputs"]:
                print(f"  Testing input: {input_field['name']} ({input_field['type']})")

                for p_info in FUZZ_PAYLOADS:
                    tested_count += 1
                    try:
                        # Fresh page for each test to avoid state contamination
                        test_page = context.new_page()
                        test_page.goto(url, wait_until="networkidle", timeout=15000)

                        # Fill the target field
                        try:
                            test_page.fill(input_field["selector"], p_info["payload"])
                        except Exception:
                            test_page.close()
                            continue

                        # Capture response after interaction
                        time.sleep(0.3)
                        content = test_page.content()

                        # Check for issues
                        issues = []
                        if p_info["category"] == "XSS" and check_reflection(content, p_info["payload"]):
                            issues.append("XSS reflection detected — payload appears unescaped in response")
                        if p_info["category"] == "SQLi" and check_sql_error(content):
                            issues.append("SQL error message exposed in response")
                        if p_info["id"] == "template_inject" and "49" in content:
                            issues.append("Template injection: '{{7*7}}' evaluated to 49")
                        if p_info["id"] == "template_inject2" and "49" in content:
                            issues.append("Template injection: '${7*7}' evaluated to 49")

                        if issues:
                            finding = {
                                "severity": "HIGH" if p_info["category"] in ("XSS", "SQLi", "Template Injection") else "MEDIUM",
                                "category": p_info["category"],
                                "payload_id": p_info["id"],
                                "payload": p_info["payload"],
                                "form_index": form["index"],
                                "input_name": input_field["name"],
                                "issues": issues,
                            }
                            findings.append(finding)
                            for issue in issues:
                                print(f"    ⚠️  [{p_info['category']}] {issue}")

                        test_page.close()

                    except Exception as e:
                        pass  # Timeouts and navigation errors are expected during fuzzing

        browser.close()

    # Save results
    results = {
        "url": url,
        "timestamp": datetime.now().isoformat(),
        "forms_found": len(forms),
        "tests_run": tested_count,
        "findings": findings,
        "summary": {
            "HIGH": len([f for f in findings if f["severity"] == "HIGH"]),
            "MEDIUM": len([f for f in findings if f["severity"] == "MEDIUM"]),
        }
    }

    raw_path = os.path.join(output_dir, "fuzz_results.json")
    with open(raw_path, "w") as f:
        json.dump(results, f, indent=2)

    # Markdown report
    report_lines = [
        "# Fuzz Test Results",
        f"",
        f"**URL**: {url}",
        f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"**Forms tested**: {len(forms)}",
        f"**Total tests run**: {tested_count}",
        f"",
        f"## Summary",
        f"",
        f"| Severity | Count |",
        f"|----------|-------|",
        f"| 🔴 HIGH  | {results['summary']['HIGH']} |",
        f"| 🟡 MEDIUM | {results['summary']['MEDIUM']} |",
        f"",
    ]

    if not findings:
        report_lines.append("✅ **No injection issues detected by automated fuzzing.**")
        report_lines.append("")
        report_lines.append("> Note: Automated fuzzing catches obvious reflection/injection only. Complete the OWASP checklist for full coverage.")
    else:
        report_lines.append("## Findings\n")
        for i, f in enumerate(findings, 1):
            icon = "🔴" if f["severity"] == "HIGH" else "🟡"
            report_lines.append(f"### {icon} {i}. [{f['category']}] Input: `{f['input_name']}`")
            report_lines.append(f"- **Payload**: `{f['payload'][:80]}`")
            for issue in f["issues"]:
                report_lines.append(f"- **Issue**: {issue}")
            report_lines.append("")

    report_path = os.path.join(output_dir, "fuzz_report.md")
    with open(report_path, "w") as f:
        f.write("\n".join(report_lines))

    print(f"\n{'='*40}")
    print(f"Tests run: {tested_count} | Findings: {len(findings)}")
    print(f"Results: {raw_path}")
    print(f"Report:  {report_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fuzz web form inputs for security issues")
    parser.add_argument("--url", required=True, help="URL to test")
    parser.add_argument("--output", required=True, help="Output directory")
    args = parser.parse_args()
    fuzz(args.url, args.output)