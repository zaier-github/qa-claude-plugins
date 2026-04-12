---
name: a11y-guardian
description: >
  Audits web pages and components for WCAG 2.1/2.2 accessibility compliance. Use this skill
  whenever the user wants to: scan a page for accessibility violations, check ARIA attributes,
  verify color contrast ratios, test keyboard navigation, audit alt text quality, produce an
  accessibility report, check VoiceOver or NVDA or JAWS compatibility, verify screen reader
  reading order, check focus trapping, test with assistive technology, or prepare for an
  accessibility audit or legal compliance review. Trigger for phrases like "check accessibility",
  "WCAG compliance", "a11y audit", "screen reader compatible", "ADA compliance", "check color
  contrast", "contrast ratio", "is my site accessible", "axe scan", "tab order", "ARIA landmark",
  "focus order", "keyboard trap", "VoiceOver", "NVDA", or any request involving assistive
  technology compatibility. Even if the user just says "check my page" or "audit this UI",
  trigger this skill if accessibility context is present.
---

# Accessibility (A11y) Guardian

Runs systematic WCAG 2.1/2.2 compliance checks on web interfaces. You combine automated scanning (axe-core via Playwright) with structured manual checklists and, where possible, AI-assisted alt text evaluation.

## What you need to get started

- A **URL** to audit (preferred — enables automated scanning)
- OR HTML source / component code (enables static analysis)

A target WCAG level is also helpful (A, AA, or AAA). Default to **AA** if not specified — this is the legal standard in most jurisdictions.

## Workflow

### Step 1: Automated scan with axe-core

Run the axe scanner:
```bash
python scripts/axe_scan.py --url <URL> --output /tmp/a11y-results/
```

This produces:
- `axe_results.json` — raw violations data
- `axe_report.md` — human-readable summary

The scanner checks for ~100+ WCAG rules including: missing alt text, insufficient color contrast, form labels, ARIA misuse, focus management, and heading hierarchy.

### Step 2: Manual checks from the checklist

Automated tools catch ~30-40% of accessibility issues. Read `references/manual-checklist.md` and work through each item that applies to the page type being audited. Key items that axe *cannot* check:

- **Keyboard navigation**: Can the entire page be operated with Tab, Shift+Tab, Enter, Escape, and arrow keys?
- **Focus visibility**: Is the keyboard focus indicator always visible (not just the browser default)?
- **Logical reading order**: Does the DOM order match the visual order? Would a screen reader announce content in the right sequence?
- **Meaningful link text**: Are links like "click here" or "read more" acceptable in context, or are they ambiguous without surrounding text?
- **Error recovery**: When a form has errors, are they clearly described and is focus moved to the error?
- **Timeout warnings**: If the page has session timeouts, does it warn users before expiry?

### Step 3: Alt text quality check (when images are present)

If the page contains `<img>` tags, evaluate alt text quality. For each significant image (non-decorative), assess:
- Is alt text present?
- Is it descriptive enough to convey the image's purpose (not just its appearance)?
- For functional images (buttons with icons), does the alt text describe the *action*, not the icon?
- Are purely decorative images using `alt=""` or `role="presentation"`?

If vision capability is available, describe each image and compare your description to the existing alt text. Flag cases where the alt text is misleading, too generic, or missing.

### Step 4: Produce the accessibility report

Use `references/a11y-report-template.md`. WCAG violations map to impact levels:

| Impact | Meaning |
|--------|---------|
| 🔴 Critical | Completely blocks access for some users — fix before shipping |
| 🟠 Serious | Significantly impairs experience — fix before shipping |
| 🟡 Moderate | Causes difficulty — fix in next sprint |
| 🟢 Minor | Annoyance, best practice — fix when possible |

Structure the report by: automated findings → manual findings → alt text findings → summary score.

## Color contrast quick reference

WCAG AA requires:
- Normal text (< 18pt / < 14pt bold): **4.5:1** minimum contrast ratio
- Large text (≥ 18pt / ≥ 14pt bold): **3:1** minimum
- UI components and graphical objects: **3:1** minimum

WCAG AAA requires 7:1 for normal text, 4.5:1 for large text.

## Common false positives to watch for

- axe may flag contrast on elements that are never visible (hidden with `display:none` or `visibility:hidden`) — verify elements are actually rendered before reporting
- `aria-hidden="true"` on decorative elements is correct, not a violation
- Some third-party widgets have known accessibility issues that can't be fixed without forking — note these separately

## Reference files

- `references/manual-checklist.md` — Structured WCAG 2.1/2.2 manual testing checklist
- `references/a11y-report-template.md` — Report output format
- `scripts/axe_scan.py` — Automated axe-core scanning via Playwright