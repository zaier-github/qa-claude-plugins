# Testing Heuristics Cheatsheet
## Quick reference for exploratory testing

---

## Input / Data Heuristics

### BINMEN (boundary testing)
Test these values for every input field:
- **B**oundary values (min, max, exactly at limit)
- **I**nvalid values (wrong type, out of range)
- **N**ull / empty / blank
- **M**ax length (and one over)
- **E**xample data (real-looking but fake)
- **N**egative numbers

### "Goldilocks" rule
Too small → just right → too large
Test one under, at, and one over every threshold.

---

## Workflow / State Heuristics

### "Interrupt mid-flow"
In any multi-step process, interrupt it at each step:
- Press Back
- Refresh the page
- Open in a new tab
- Close and reopen
- Let the session expire
- Open the same flow twice simultaneously

### CRUD completeness
For any entity, verify all four operations work:
- **C**reate
- **R**ead (view, search, list)
- **U**pdate (partial and full)
- **D**elete (and what happens to related data)

### State machine coverage
For features with statuses/states (e.g., Order: pending → shipped → delivered):
- Test every valid transition
- Test every *invalid* transition (can you go delivered → pending?)
- Test what happens in each state (can you edit a delivered order?)

---

## User Perspective Heuristics

### "The 5 types of users"
- **New user** — first visit, no data, no history
- **Power user** — lots of data, complex configuration, muscle memory
- **Distracted user** — opens multiple tabs, takes a long time, gets interrupted
- **Adversarial user** — tries to break things, inputs weird data, manipulates URLs
- **Accessibility user** — keyboard only, screen reader, high contrast mode

### "What would Grandma do?"
Would a non-technical user understand every error message? Every label? Every confirmation dialog?

---

## System / Integration Heuristics

### "Downstream effects"
When you perform an action, what else happens?
- Is an email sent?
- Is a record created/updated elsewhere?
- Is an event logged?
- Is a third-party system notified?
- Test that each downstream effect fires exactly once.

### "The seams"
Bugs cluster at integration points. Specifically test:
- API request/response boundaries
- Database read/write roundtrips (does what you save match what you retrieve?)
- Third-party service calls (what happens when they're slow? Down? Return unexpected data?)

---

## Time-Based Heuristics

### "Clock edge cases"
- Midnight (00:00 → 00:01)
- End of month (Jan 31 → Feb 1)
- Leap day (Feb 29)
- End of year (Dec 31 → Jan 1)
- Daylight Saving transitions (clocks spring forward / fall back)
- Unix epoch (1970-01-01) and "Y2K38" (2038-01-19)

### "Patience testing"
- Leave a session idle until it expires, then try to act
- Submit a slow form after the server-side lock might have expired
- Open a confirmation dialog for a very long time before confirming

---

## Bug Cluster Heuristics

### "Where bugs travel"
When you find a bug, check these related areas:
- **Same feature, different data**: Does the bug happen with other input values?
- **Same component, different feature**: Does the same UI component have the bug elsewhere?
- **Same code path, different user role**: Does the bug only affect some roles?
- **Sibling functionality**: If Delete is broken, check Edit and Create too
- **Inverse action**: If Create fails silently, does Delete also fail silently?

### "Error handling completeness"
If you find that one error state is handled poorly (bad message, no message, crash), check all error states for the same feature:
- Network timeout
- Server error (500)
- Validation error
- Authorization error (403)
- Not found (404)
- Conflict (409)

---

## "Oracles" — How do you know if a test passed?

An oracle is how you judge correctness. Use multiple:

| Oracle type | Example |
|-------------|---------|
| **Spec/requirements** | "The spec says it should do X" |
| **Consistency** | "It behaved differently than last time" |
| **Comparable product** | "The competitor does it differently" |
| **User expectation** | "A user would expect X here" |
| **Common sense** | "This output makes no sense" |
| **History** | "This used to work differently" |
| **Internal consistency** | "The total doesn't add up to the line items" |