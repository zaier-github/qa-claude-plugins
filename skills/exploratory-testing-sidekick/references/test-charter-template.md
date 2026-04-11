# Test Charter: {{FEATURE NAME}}

**Date**: {{DATE}}
**Tester**: {{NAME}}
**Feature / PR**: {{LINK OR DESCRIPTION}}
**Charter duration**: {{e.g., 60 minutes}}

---

## Feature Summary

{{One paragraph: what this feature does, who uses it, why it exists}}

---

## Test Focus

{{What specific aspect of this feature are you testing in this charter?
 E.g., "Focus: Input validation and error handling for the signup form"}}

---

## Risks (What Worries Me Most)

1. {{Risk: what could go wrong and why you're concerned}}
2. ...

---

## SFDPOT Test Ideas

### [S] Structure — What is this made of?
- [ ] {{e.g., "Verify all form fields are labeled correctly"}}
- [ ] ...

### [F] Function — What does it do?
- [ ] {{e.g., "Verify that clicking 'Save' creates a new record"}}
- [ ] ...

### [D] Data — What data does it handle?
- [ ] {{e.g., "Submit with empty required fields"}}
- [ ] {{e.g., "Submit with a 256-character name"}}
- [ ] {{e.g., "Submit with emoji in text fields"}}
- [ ] ...

### [P] Platform — Where does it run?
- [ ] {{e.g., "Test on Safari (iOS) — mobile layout"}}
- [ ] {{e.g., "Test with slow 3G throttling"}}
- [ ] ...

### [O] Operations — How will users actually use it?
- [ ] {{e.g., "Press browser Back mid-flow"}}
- [ ] {{e.g., "Open in two tabs simultaneously"}}
- [ ] ...

### [T] Time — What breaks over time?
- [ ] {{e.g., "Leave the form idle for 30 minutes then submit"}}
- [ ] {{e.g., "Test with a date of Feb 29 (leap year boundary)"}}
- [ ] ...

---

## Interesting Scenarios

_Story-form test cases: describe who is doing what, and what you're checking._

**Scenario 1 — {{Name}}**:
{{2–3 sentence story: e.g., "A new user signs up using a Gmail address with a '+' subaddress (user+test@gmail.com). They complete registration and expect to receive a confirmation email. We're checking that the subaddress is preserved correctly and not stripped."}}

**Scenario 2 — {{Name}}**:
{{...}}

**Scenario 3 — {{Name}}**:
{{...}}

---

## Out of Scope (for this charter)

- {{What you're NOT testing here, and why}}
- ...

---

## Notes / Observations

{{Fill in during and after testing}}

---

## Bugs Found

| ID | Summary | Severity |
|----|---------|---------|
| | | |