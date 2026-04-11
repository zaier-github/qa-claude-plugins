# Coverage Risk Map: [Project / Module Name]

> **Analyzed:** YYYY-MM-DD | **Stack:** [Language / Framework]
> **Coverage source:** [lcov / Istanbul / pytest-cov / estimated / etc.]
> **Scope:** [Full codebase / Module X / Service Y]

---

## Executive Summary

_2–4 sentences. What is the overall test debt posture? What is the single most dangerous
gap? What would a focused sprint of test writing accomplish?_

**Overall coverage:** X% line / Y% branch _(or: estimated)_
**Gaps analyzed:** N files / N functions across N tiers
**Most critical gap:** [One sentence naming the highest-risk untested path]

---

## 🔴 Danger Zone

_Untested code that is highly likely to cause a production incident. Address in the current
or next sprint. Each entry is a specific gap, not a general area._

### D-001 · `path/to/file.py` · `function_or_class`

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Change Velocity | 3 | 12 commits in 90 days |
| Feature Reach | 3 | Imported by 18 files |
| Failure Impact | 3 | Writes to billing DB |
| Domain Criticality | 3 | Payments domain |
| **Composite** | **3.0** | |

**What's uncovered:** [Specific uncovered branches, functions, or scenarios]

**Why it matters:** [In plain language — what breaks in production if this has a bug]

**Recommended test(s):**
- [ ] [Specific test scenario, e.g., "Integration test: apply coupon to subscription renewal with expired card on file"]
- [ ] [Another specific scenario if warranted]

---

### D-002 · `path/to/file.py` · `function_or_class`

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Change Velocity | | |
| Feature Reach | | |
| Failure Impact | | |
| Domain Criticality | | |
| **Composite** | | |

**What's uncovered:**

**Why it matters:**

**Recommended test(s):**
- [ ]

---

## 🟠 Watch List

_Significant gaps that should be addressed in the next 1–2 sprints. Real risk, slightly
lower urgency than Danger Zone._

### W-001 · `path/to/file.py` · `function_or_class`

**Composite score:** X.X | **Key risk factor:** [e.g., "Wide reach: 14 importers"]

**What's uncovered:** [Specific gaps]

**Recommended test(s):**
- [ ]

---

<!-- Add more Watch List entries -->

---

## 🟡 Backlog

_Real debt but lower urgency. Capture for future sprint planning. Brief entries are fine._

| File / Module | Coverage | Key Risk Factor | Recommended Action |
|--------------|----------|-----------------|-------------------|
| `path/to/file.py` | 15% | High velocity | Add unit tests for X and Y |
| `path/to/other.py` | 0% | Isolated, stable | Low urgency; document and revisit |

---

## 🟢 Low Priority

_Note these exist. No action needed this cycle._

| File / Module | Coverage | Why Low Priority |
|--------------|----------|-----------------|
| `path/to/helper.py` | 0% | Formatting only, no logic, stable |

---

## Structural Patterns Found

_Systemic issues beyond individual gaps. These explain *why* gaps exist and suggest process
or architectural changes alongside tactical test writing._

### [Pattern Name] — [🔴/🟠/🟡 Severity]

**Where:** [Which files, modules, or domains exhibit this pattern]

**What it means:** [Why this pattern is risky]

**Structural recommendation:** [What would fix this at the system level, not just tactically]

---

<!-- Repeat for each pattern found. If none, remove this section. -->

---

## Recommended Coverage Sprint

_A concrete, scoped list of the highest-ROI tests to write in one sprint. Ordered by
impact. Estimated complexity is rough: S = <1 hour, M = half day, L = full day._

| Priority | File / Function | Test to Write | Complexity | Tier Addressed |
|----------|----------------|---------------|------------|----------------|
| 1 | `billing/processor.py::charge_card` | Integration: charge with expired card | M | 🔴 D-001 |
| 2 | `auth/session.py::refresh_token` | Unit: null token, expired token, concurrent refresh | S | 🔴 D-002 |
| 3 | `checkout/flow.py` (E2E) | Smoke test: guest checkout end-to-end | L | 🟠 W-001 |

**Sprint goal:** Completing these N tests would move X Danger Zone gaps to covered and
address the [pattern name] structural pattern.

---

## What Good Looks Like

_Domain-specific targets for this codebase. Not one-size-fits-all percentages._

| Domain | Recommended Line Coverage | Recommended Branch Coverage | Notes |
|--------|--------------------------|----------------------------|-------|
| Payments / Billing | ≥90% | ≥85% | Every error path must be tested |
| Auth / Session | ≥90% | ≥85% | Security-critical; no gaps acceptable |
| Core business logic | ≥80% | ≥70% | |
| API handlers / routes | ≥75% | ≥60% | |
| Utilities / helpers | ≥60% | ≥50% | |
| Internal tooling / scripts | ≥40% | — | Lower bar; not user-facing |

---

## Methodology Notes

_Any assumptions, approximations, or limitations in this analysis._

- Coverage data source: [tool and version]
- Git history range used for velocity scoring: [e.g., "90 days"]
- Files excluded from analysis: [if any]
- Dimensions approximated (no direct measurement): [if any]

---

*Generated by Test Debt Cartographer skill | YYYY-MM-DD*