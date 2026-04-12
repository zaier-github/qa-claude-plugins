# Manual Accessibility (A11y) Checklist
## WCAG 2.1 / 2.2 — Level AA

Automated tools (axe-core, Lighthouse) catch ~30-40% of issues. This checklist covers what they miss.
Check each item applicable to the page type. Mark: ✅ Pass | ❌ Fail | ⚠️ Partial | N/A

---

## 1. Keyboard Navigation

| # | Check | Notes |
|---|-------|-------|
| K1 | All interactive elements are reachable by Tab key | Buttons, links, inputs, selects, custom controls |
| K2 | Tab order follows logical reading order | Left-to-right, top-to-bottom in LTR languages |
| K3 | No keyboard traps — Tab always allows escape | Especially in modals, date pickers, custom dropdowns |
| K4 | Modal dialogs trap focus within themselves while open | Tab should cycle within the modal |
| K5 | Escape key closes modals, tooltips, and dropdowns | |
| K6 | Arrow keys navigate within composite widgets | Menus, radio groups, tabs, sliders |
| K7 | Skip navigation link is present and functional | "Skip to main content" link visible on focus |

## 2. Focus Visibility

| # | Check | Notes |
|---|-------|-------|
| F1 | Focus indicator is visible on all interactive elements | Not just browser default — check custom styles |
| F2 | Focus indicator meets 3:1 contrast against adjacent colors | WCAG 2.2 new requirement |
| F3 | Focus is never moved unexpectedly without user action | |
| F4 | After closing a modal, focus returns to the triggering element | |

## 3. Screen Reader Compatibility

| # | Check | Notes |
|---|-------|-------|
| SR1 | Page has a descriptive `<title>` | Unique per page, not just the site name |
| SR2 | Headings form a logical hierarchy (h1 → h2 → h3...) | No skipped levels except for styling purposes |
| SR3 | Landmark regions are used (`<main>`, `<nav>`, `<header>`, `<footer>`) | |
| SR4 | All form inputs have associated `<label>` elements | Placeholder alone is not sufficient |
| SR5 | Error messages are programmatically associated with inputs | Use `aria-describedby` or `aria-errormessage` |
| SR6 | Dynamic content changes are announced | Use `aria-live` for status messages, alerts |
| SR7 | Icons and SVGs have accessible text | `aria-label`, `title`, or hidden text |
| SR8 | Decorative images use `alt=""` | Not `alt="decorative"` — literally empty |

## 4. Color and Contrast

| # | Check | Notes |
|---|-------|-------|
| C1 | Normal text contrast ≥ 4.5:1 | < 18pt regular or < 14pt bold |
| C2 | Large text contrast ≥ 3:1 | ≥ 18pt regular or ≥ 14pt bold |
| C3 | UI components contrast ≥ 3:1 | Buttons, inputs, focus indicators |
| C4 | Information is not conveyed by color alone | Red/green status also has icon or text |
| C5 | Links are distinguishable from surrounding text | Underline or other non-color cue |

## 5. Forms

| # | Check | Notes |
|---|-------|-------|
| FM1 | Required fields are clearly marked | Not just color — use text or `*` with legend |
| FM2 | Form errors are announced clearly | Inline errors near the field, not just at top |
| FM3 | Focus moves to first error after failed submission | |
| FM4 | Autocomplete attributes used for personal data fields | name, email, address, etc. |
| FM5 | Sufficient time to complete forms if timed | Or warning with ability to extend |

## 6. Images and Media

| # | Check | Notes |
|---|-------|-------|
| M1 | All informative images have descriptive alt text | |
| M2 | Complex images (charts, diagrams) have extended descriptions | Figure caption or longdesc |
| M3 | Videos have captions | Synchronized, accurate captions |
| M4 | Audio content has transcripts | |
| M5 | No content flashes more than 3 times per second | Seizure risk |
| M6 | Autoplay audio can be paused or stopped | |

## 7. Links and Buttons

| # | Check | Notes |
|---|-------|-------|
| L1 | Link text is meaningful out of context | Not "click here" or "read more" |
| L2 | Links opening new tabs warn users | e.g., "(opens in new tab)" |
| L3 | Buttons describe the action they perform | Not just "submit" when the action is "Create account" |
| L4 | Identical links with different destinations have distinguishable text | |

## 8. Mobile / Touch

| # | Check | Notes |
|---|-------|-------|
| T1 | Touch targets are at least 24×24px (WCAG 2.2) | 44×44px recommended |
| T2 | Sufficient spacing between touch targets | Accidental activation is hard |
| T3 | Functionality works in both portrait and landscape | |
| T4 | Page is not locked to one orientation | Unless essential |

## 9. Cognitive Accessibility

| # | Check | Notes |
|---|-------|-------|
| COG1 | Instructions do not rely solely on sensory characteristics | Not "click the round button on the left" |
| COG2 | Session timeouts warn users ≥ 20 seconds before expiry | |
| COG3 | Input errors provide suggestions for correction | If format is known (e.g., phone number) |
| COG4 | Confirmation step for important/irreversible actions | Delete, purchase, send |

---

## How to use this checklist

1. Work through each section applicable to the page being tested
2. Use keyboard only — put your mouse away for keyboard navigation checks
3. Use a screen reader for SR checks — NVDA (Windows/free), VoiceOver (macOS/iOS/free), or JAWS (Windows/paid)
4. Record failures with: element location, screenshot/video, and the WCAG success criterion violated