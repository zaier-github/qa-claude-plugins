---
name: security-chaos-monkey
description: >
  Performs lightweight security testing during QA to catch low-hanging-fruit vulnerabilities before
  code ships. Use this skill whenever a QA engineer or developer wants to: fuzz input fields for
  XSS/SQLi/injection vulnerabilities, scan dependency files for known CVEs, check for exposed secrets
  in browser console or network traffic, review OWASP Top 10 risks for a feature, or add a security
  sanity-check step to a PR review workflow. Trigger for phrases like "check for security issues",
  "fuzz test", "XSS test", "SQL injection", "CVE scan", "dependency vulnerabilities", "security QA",
  "OWASP", "pentest light", "check for secrets in the console", or any request for basic security
  validation during QA. This is NOT a replacement for a professional pentest — make that clear.
---

# Security Chaos Monkey (Lightweight)

Proactively hunts for "low-hanging fruit" security vulnerabilities during QA. You perform the basic security checks that catch common bugs before they reach production — input validation failures, dependency vulnerabilities, and exposed secrets. You are not a penetration tester; you are QA's first line of defense.

> ⚠️ **Scope**: This skill is for finding your *own* application's bugs in a *test environment* you have permission to test. Never run these tests against systems you don't own or have written authorization to test.

## What you can test

1. **Input field fuzzing** — XSS, SQL injection, command injection, path traversal
2. **Dependency CVE scanning** — `package.json`, `requirements.txt`, `Pipfile`, `pom.xml`, `Gemfile`
3. **Exposed secrets detection** — browser console logs, network responses, HTML source
4. **Security headers check** — CSP, HSTS, X-Frame-Options, etc.
5. **OWASP Top 10 checklist review** — guided assessment of a feature against the top risks

## Workflow

### Option A: Input field fuzzing (URL required)

```bash
python scripts/fuzz_inputs.py --url <URL> --output /tmp/fuzz-results/
```

The fuzzer finds forms on the page, submits payloads from `references/fuzz-payloads.md` into each field, and reports which payloads caused unexpected behavior (reflected content, errors, unusual responses).

**What it checks:**
- XSS reflection: does the payload appear unescaped in the response?
- SQL error exposure: do error messages reveal DB queries or stack traces?
- Command injection: do shell metacharacters trigger errors?
- Path traversal: do `../` sequences cause different responses?

After fuzzing, review the results report and investigate any flagged inputs manually.

### Option B: CVE scan on dependency files

```bash
python scripts/scan_dependencies.py --file <path/to/package.json|requirements.txt> --output /tmp/cve-results/
```

This uses the OSV (Open Source Vulnerability) database API — no API key required. It outputs:
- A list of vulnerable packages with CVE IDs and severity
- Recommended upgrade versions where available
- A severity summary (critical/high/medium/low counts)

For CI integration, add this as a PR check step.

### Option C: OWASP Top 10 checklist review

Load `references/owasp-top10-checklist.md` and work through the checklist for the feature being tested. Each item includes:
- What the risk is (one sentence)
- What to check in QA
- What a vulnerable response looks like

Mark each item: ✅ Checked & OK | ❌ Potential issue | ⚠️ Couldn't verify | N/A

Produce a summary report with the items that need developer attention.

### Option D: Security headers check (URL required)

```bash
python scripts/check_headers.py --url <URL>
```

Checks for presence and correctness of: `Content-Security-Policy`, `Strict-Transport-Security`, `X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy`, `Permissions-Policy`.

## Responsible use guidelines

- Only test applications you own or have explicit written permission to test
- Run tests in a staging/test environment, not production
- Some payloads (like SQL injection strings) may trigger WAF blocks or security alerts — be aware
- Do not store, share, or act on any real user data you incidentally encounter
- Report findings to your security team, not just in a bug tracker

## Reference files

- `references/fuzz-payloads.md` — Curated XSS, SQLi, and injection payloads for QA
- `references/owasp-top10-checklist.md` — OWASP Top 10 QA checklist
- `scripts/fuzz_inputs.py` — Form fuzzing script (Playwright-based)
- `scripts/scan_dependencies.py` — Dependency CVE scanner (OSV API)
- `scripts/check_headers.py` — Security headers checker