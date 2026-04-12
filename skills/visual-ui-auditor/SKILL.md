---
name: visual-ui-auditor
description: >
  Audits web UIs for visual consistency, design system compliance, dark patterns, and layout shifts.
  Use this skill whenever the user wants to: check a webpage against a design system or style guide,
  compare screenshots to a golden standard, detect UI regressions, flag accessibility-adjacent visual
  issues (low contrast, hidden buttons, misleading affordances), or catch layout shifts during page
  load. Trigger this skill for requests like "check my UI matches the design", "compare these
  screenshots", "find dark patterns", "visual regression test", "does my page follow brand guidelines",
  or any task involving systematic visual inspection of a web interface.
---

# Visual UI/UX Auditor

Audits web interfaces for design consistency, brand compliance, and deceptive patterns. You go beyond pixel-matching — you understand *intent* and *design system rules*, flagging both objective violations (wrong color) and subjective concerns (hidden unsubscribe buttons).

## What you need to get started

You need at least one of:
- A URL to audit live (uses Playwright to capture)
- A screenshot or set of screenshots
- A design system spec (JSON, CSS file, or described in prose)

If none of these are supplied, ask for them before proceeding. A design system spec is optional but greatly improves audit quality — without one, you'll focus on general UI heuristics.

## Workflow

### Step 1: Capture the UI

If given a URL, use the capture script to take screenshots:
```bash
python scripts/capture_ui.py --url <URL> --output /tmp/ui-capture/
```

This captures: full-page screenshot, viewport screenshot, and any visible modals/overlays after a short wait. It also dumps computed CSS for key interactive elements (buttons, links, forms).

If screenshots are already provided, skip capture and work directly with those images.

### Step 2: Load the design system

Read `references/design_system_template.json` as your baseline. If the user provides their own design spec, use that instead — it overrides the template completely.

Instantiate the rules you'll check against. The key rule categories are:
- **Color**: primary/secondary/error/success hex values
- **Typography**: font families, sizes, weights per heading level
- **Spacing**: margin/padding scale (typically 4px or 8px grid)
- **Components**: button styles, form element appearance, modal behavior

### Step 3: Run the audit

Analyze the captured UI against the design system. Check each category systematically:

**Color compliance** — Do primary action buttons use the correct background? Are error states using the error color? Run the color extractor if needed:
```bash
python scripts/color_extractor.py --image /tmp/ui-capture/viewport.png
```

**Typography** — Are headings visually consistent? Do body text sizes match the scale?

**Component audit** — Do buttons have consistent padding, border-radius, and hover states? Are form inputs styled uniformly?

**Dark pattern detection** — Look specifically for:
- CTA buttons significantly more prominent than "cancel" / "decline" options
- Pre-checked opt-in checkboxes
- Hard-to-find unsubscribe or delete account paths
- "Confirm-shaming" language (e.g., "No thanks, I don't want to save money")
- Misleading link styling (non-links styled as buttons, buttons styled as links)

**Layout shift check** — If a URL was provided and multiple screenshots were captured at different load stages, compare them for Cumulative Layout Shift (CLS) indicators.

### Step 4: Produce the audit report

Use the report template at `references/audit_report_template.md`. Fill in every section. Severity levels:

| Level | Meaning |
|-------|---------|
| 🔴 Critical | Brand violation or deceptive pattern — fix before shipping |
| 🟡 Warning | Inconsistency that erodes polish — fix in next sprint |
| 🟢 Info | Minor deviation or suggestion — consider fixing |

Always include:
- A summary count: "X critical, Y warnings, Z info"
- A screenshot annotation or reference for each finding (describe location clearly if you can't annotate directly)
- Specific remediation for each finding

## Tips for thorough audits

- Check **both desktop and mobile viewports** if possible — many design system violations only appear at one breakpoint
- Interactive elements (hover states, focus rings) often get missed — if you can capture them, do
- When no design system is provided, compare elements *against each other* for internal consistency — a page should at least be consistent with itself
- Dark patterns are a judgment call; flag them as "potential" if uncertain and explain your reasoning

## Reference files

- `references/design_system_template.json` — Default design system schema to audit against; replace with user's own spec
- `references/audit_report_template.md` — Report output format
- `scripts/capture_ui.py` — Playwright-based UI capture
- `scripts/color_extractor.py` — Extracts dominant colors from screenshots using Pillow