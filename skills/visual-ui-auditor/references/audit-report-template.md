# UI Audit Report: {{PAGE_OR_COMPONENT_NAME}}

**Audited**: {{DATE}}
**URL / Source**: {{URL_OR_FILE}}
**Design System**: {{DESIGN_SYSTEM_NAME_OR_"General heuristics"}}
**Viewport(s) tested**: {{e.g., "1440px desktop, 375px mobile"}}

---

## Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | {{N}} |
| 🟡 Warning  | {{N}} |
| 🟢 Info     | {{N}} |

**Overall verdict**: {{One sentence — e.g., "The UI has 2 brand-breaking color violations and a potential dark pattern; remaining issues are minor polish."}}

---

## Findings

### 🔴 Critical Issues

#### C1: {{Issue title}}
- **Location**: {{Describe where on the page — e.g., "Primary CTA button in hero section"}}
- **Finding**: {{What is wrong}}
- **Expected**: {{What the design system or best practice requires}}
- **Actual**: {{What was observed — include hex/px values if applicable}}
- **Remediation**: {{Specific fix}}

*(Repeat for each critical issue)*

---

### 🟡 Warnings

#### W1: {{Issue title}}
- **Location**: {{...}}
- **Finding**: {{...}}
- **Remediation**: {{...}}

*(Repeat for each warning)*

---

### 🟢 Info / Suggestions

#### I1: {{Issue title}}
- **Location**: {{...}}
- **Suggestion**: {{...}}

*(Repeat for each info item)*

---

## Dark Pattern Assessment

{{If no dark patterns were found: "No dark patterns detected."}}

{{If found, describe each one:}}
#### DP1: {{Pattern name}} — {{Potential / Confirmed}}
- **Location**: {{...}}
- **Description**: {{What the pattern is and why it's problematic}}
- **Severity**: 🔴 / 🟡
- **Remediation**: {{...}}

---

## Layout / CLS Notes

{{If URL was tested and load stages captured:}}
- {{Describe any elements that shifted between load stages}}
- {{Note specific components that appeared late and caused reflow}}

{{If not applicable: "Layout shift analysis not performed (no URL provided or single screenshot only)."}}

---

## Appendix: Design System Rules Checked

| Category | Rules checked | Violations |
|----------|--------------|------------|
| Colors | {{N}} | {{N}} |
| Typography | {{N}} | {{N}} |
| Spacing | {{N}} | {{N}} |
| Components | {{N}} | {{N}} |
| Dark patterns | {{N}} | {{N}} |