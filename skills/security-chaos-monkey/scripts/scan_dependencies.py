#!/usr/bin/env python3
"""
scan_dependencies.py — Scan package dependency files for known CVEs using the OSV database.
Usage: python scripts/scan_dependencies.py --file <package.json|requirements.txt> --output <dir>

Uses the free OSV (Open Source Vulnerability) API — no API key required.
Supports: package.json, requirements.txt, Pipfile (basic), yarn.lock (names only)
"""
import argparse
import json
import os
import re
import sys
import urllib.request
import urllib.parse
from datetime import datetime

OSV_BATCH_URL = "https://api.osv.dev/v1/querybatch"


def parse_package_json(path: str) -> list[dict]:
    with open(path) as f:
        data = json.load(f)
    packages = []
    for section in ("dependencies", "devDependencies", "peerDependencies"):
        for name, version in data.get(section, {}).items():
            # Strip semver range prefixes: ^1.2.3 → 1.2.3
            version = re.sub(r'^[\^~>=<*]+', '', version).strip()
            if version and version != "latest" and version != "*":
                packages.append({"name": name, "version": version, "ecosystem": "npm", "section": section})
    return packages


def parse_requirements_txt(path: str) -> list[dict]:
    packages = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or line.startswith("-"):
                continue
            # Handle: package==1.2.3, package>=1.2.3, package[extra]==1.2.3
            match = re.match(r'^([A-Za-z0-9_\-\.\[\]]+)[>=<!\s]+([0-9][^\s,;#]*)', line)
            if match:
                name = re.sub(r'\[.*\]', '', match.group(1))  # strip extras
                version = match.group(2).strip()
                packages.append({"name": name, "version": version, "ecosystem": "PyPI", "section": "dependencies"})
    return packages


def parse_dependency_file(path: str) -> list[dict]:
    filename = os.path.basename(path).lower()
    if filename == "package.json":
        return parse_package_json(path)
    elif filename in ("requirements.txt", "requirements-dev.txt", "requirements-test.txt"):
        return parse_requirements_txt(path)
    elif filename == "pipfile":
        # Basic Pipfile parsing (no TOML library needed)
        packages = []
        with open(path) as f:
            content = f.read()
        for match in re.finditer(r'([a-zA-Z0-9_\-]+)\s*=\s*"([^"]+)"', content):
            version = re.sub(r'^[\^~>=<*]+', '', match.group(2)).strip()
            if version and version != "*":
                packages.append({"name": match.group(1), "version": version, "ecosystem": "PyPI", "section": "dependencies"})
        return packages
    else:
        print(f"Unsupported file type: {filename}. Supported: package.json, requirements.txt, Pipfile")
        sys.exit(1)


def query_osv(packages: list[dict]) -> dict:
    """Query OSV batch API for vulnerabilities."""
    queries = []
    for pkg in packages:
        queries.append({
            "package": {
                "name": pkg["name"],
                "ecosystem": pkg["ecosystem"]
            },
            "version": pkg["version"]
        })

    # OSV batch limit is 1000 — chunk if needed
    all_results = []
    chunk_size = 100
    for i in range(0, len(queries), chunk_size):
        chunk = queries[i:i + chunk_size]
        body = json.dumps({"queries": chunk}).encode()
        req = urllib.request.Request(
            OSV_BATCH_URL,
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read())
                all_results.extend(data.get("results", []))
        except Exception as e:
            print(f"OSV API error: {e}")
            all_results.extend([{}] * len(chunk))

    return all_results


SEVERITY_ORDER = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3, "UNKNOWN": 4}

def extract_severity(vuln: dict) -> str:
    for sev in vuln.get("severity", []):
        score_text = sev.get("score", "")
        if "CRITICAL" in score_text.upper():
            return "CRITICAL"
        elif "HIGH" in score_text.upper():
            return "HIGH"
        elif "MEDIUM" in score_text.upper():
            return "MEDIUM"
        elif "LOW" in score_text.upper():
            return "LOW"
    # Fallback: check CVSS score
    for affected in vuln.get("affected", []):
        for severity in affected.get("severity", []):
            score = severity.get("score", "")
            try:
                cvss = float(score)
                if cvss >= 9.0: return "CRITICAL"
                if cvss >= 7.0: return "HIGH"
                if cvss >= 4.0: return "MEDIUM"
                return "LOW"
            except (ValueError, TypeError):
                pass
    return "UNKNOWN"


def scan(file_path: str, output_dir: str) -> None:
    os.makedirs(output_dir, exist_ok=True)

    print(f"Parsing: {file_path}")
    packages = parse_dependency_file(file_path)
    print(f"Found {len(packages)} packages to check")

    if not packages:
        print("No packages found to scan.")
        return

    print("Querying OSV vulnerability database...")
    osv_results = query_osv(packages)

    findings = []
    for pkg, result in zip(packages, osv_results):
        vulns = result.get("vulns", [])
        if vulns:
            for vuln in vulns:
                severity = extract_severity(vuln)
                findings.append({
                    "package": pkg["name"],
                    "version": pkg["version"],
                    "ecosystem": pkg["ecosystem"],
                    "section": pkg.get("section", ""),
                    "vuln_id": vuln.get("id", "UNKNOWN"),
                    "summary": vuln.get("summary", ""),
                    "severity": severity,
                    "details_url": f"https://osv.dev/vulnerability/{vuln.get('id', '')}",
                    "aliases": vuln.get("aliases", []),
                })

    # Sort by severity
    findings.sort(key=lambda f: SEVERITY_ORDER.get(f["severity"], 99))

    # Count by severity
    severity_counts = {s: 0 for s in SEVERITY_ORDER}
    for f in findings:
        severity_counts[f["severity"]] = severity_counts.get(f["severity"], 0) + 1

    # Save raw results
    raw = {
        "file_scanned": file_path,
        "timestamp": datetime.now().isoformat(),
        "packages_scanned": len(packages),
        "vulnerable_packages": len(set(f["package"] for f in findings)),
        "total_vulnerabilities": len(findings),
        "severity_counts": severity_counts,
        "findings": findings
    }
    raw_path = os.path.join(output_dir, "cve_results.json")
    with open(raw_path, "w") as f:
        json.dump(raw, f, indent=2)

    # Markdown report
    icon = {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡", "LOW": "🟢", "UNKNOWN": "⚪"}
    report_lines = [
        "# Dependency CVE Scan Report",
        f"",
        f"**File scanned**: `{os.path.basename(file_path)}`",
        f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"**Packages scanned**: {len(packages)}",
        f"**Vulnerable packages**: {len(set(f['package'] for f in findings))}",
        f"",
        "## Severity Summary",
        f"",
        f"| Severity | Count |",
        f"|----------|-------|",
    ]
    for sev, count in severity_counts.items():
        if count > 0:
            report_lines.append(f"| {icon.get(sev,'')} {sev} | {count} |")
    report_lines.append("")

    if not findings:
        report_lines.append("✅ **No known vulnerabilities found in scanned packages.**")
        report_lines.append("")
        report_lines.append("> Note: This scan checks against the OSV database. Always verify with your security team.")
    else:
        report_lines.append("## Vulnerabilities\n")
        for f in findings:
            i = icon.get(f["severity"], "⚪")
            aliases = f" ({', '.join(f['aliases'][:2])})" if f["aliases"] else ""
            report_lines.append(f"### {i} [{f['severity']}] {f['package']} v{f['version']}")
            report_lines.append(f"- **Vuln ID**: [{f['vuln_id']}]({f['details_url']}){aliases}")
            report_lines.append(f"- **Summary**: {f['summary']}")
            report_lines.append(f"- **Section**: {f['section']}")
            report_lines.append("")

    report_path = os.path.join(output_dir, "cve_report.md")
    with open(report_path, "w") as f:
        f.write("\n".join(report_lines))

    print(f"\n{'='*40}")
    print(f"Scanned: {len(packages)} packages | Vulnerabilities: {len(findings)}")
    for sev, count in severity_counts.items():
        if count > 0:
            print(f"  {icon.get(sev,'')} {sev}: {count}")
    print(f"\nReport: {report_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scan dependencies for CVEs via OSV")
    parser.add_argument("--file", required=True, help="Path to package.json or requirements.txt")
    parser.add_argument("--output", required=True, help="Output directory for reports")
    args = parser.parse_args()
    scan(args.file, args.output)