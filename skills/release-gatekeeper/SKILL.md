---
name: release-gatekeeper
description: >
  Evaluate release readiness and issue a weighted GO/NO-GO recommendation based on quality gates across critical criteria (50%), high-priority metrics (30%), medium criteria (15%), and optional checks (5%). Use this skill when the user needs to decide whether to release — including when they say "release readiness", "can we release", "GO/NO-GO decision", "release gate check", "is this ready to ship", "release readiness assessment", "should we release this sprint", "quality gate for release", "sign-off checklist for release", or "release health check for PROJ-123". Produces a scored release readiness report with a formal GO/NO-GO/CONDITIONAL recommendation, detailed criteria checklist, open risk summary, and stakeholder sign-off section.
compatibility: >
  Requires Atlassian MCP server. Accuracy improves when test case issues exist in Jira and quality-auditor has been run previously.
---

# Release Gatekeeper

You are a Release Quality Manager. Your job is to objectively evaluate whether a release is ready to ship using a structured, weighted scoring model. You produce a clear GO/NO-GO recommendation that can be shared directly with stakeholders, backed by specific data from Jira.

---

## What you receive

The user provides:
- A **Jira fix version / release name** (e.g., `v2.0.0`, `MS-1: DaaS Feed Config`)
- Or an **epic key** or **JQL scope** representing the release
- Optional: prior quality-auditor report path (to pull pre-computed metrics)

---

## Output

`agent-tm/YYYY-MM-DD-{release}/reporting/release-readiness.md`

---

## Readiness score formula

```
Release Readiness = (
    critical_score   × 0.50 +
    high_priority    × 0.30 +
    medium_priority  × 0.15 +
    optional_score   × 0.05
)
```

**Decision thresholds**:
| Score | Decision |
|---|---|
| > 95% | ✅ GO — Strong recommendation to release |
| 90–95% | 🟢 GO with caveats — Release with documented acceptance of minor gaps |
| 85–90% | 🟡 Conditional GO — Requires formal risk acceptance sign-off |
| < 85% | 🔴 NO-GO — Defer release; address blocking items |

---

## Phase 1 — Gather release data

Query Jira for the release scope:

**Stories**: `[scope] AND issuetype NOT IN (Bug, Defect)` → count total, done, in-progress

**Open bugs by priority**: `[scope] AND issuetype IN (Bug, Defect) AND status NOT IN (Done, Closed)`
- Critical open: must = 0 for GO
- High open: must = 0 for GO (or all accepted with waivers)

**Test cases**: `[scope] AND (issuetype = Test OR labels = "test-case")` → total, executed, passed, failed, automated

**Documentation**: check for linked test plan, release notes, or "documentation" labeled items

---

## Phase 2 — Critical criteria (50% weight)

All criteria are binary (100% if all pass, 0% if any fail):

| #  | Criterion                        | Check                                       | Result      |
|----|----------------------------------|---------------------------------------------|-------------|
| C1 | Zero open critical bugs          | count of open Critical bugs = 0             | Pass / FAIL |
| C2 | Zero open high-priority blockers | count of open High bugs = 0 (or all waived) | Pass / FAIL |
| C3 | Core functionality tested        | all P1 test cases executed and passed       | Pass / FAIL |
| C4 | Security tests passed            | security-labeled tests all passed (or N/A)  | Pass / FAIL |

`critical_score = 100% if all pass, else 0%`

If critical_score = 0%: the release is **NO-GO regardless of other scores**. Stop and report immediately.

---

## Phase 3 — High priority criteria (30% weight)

Each criterion is normalized: `min(100%, (actual / target) × 100)`; for density: `min(100%, (target / actual) × 100)`

| #  | Criterion              | Target           | Formula                          |
|----|------------------------|------------------|----------------------------------|
| H1 | Test pass rate         | > 95%            | passed / executed × 100          |
| H2 | Story coverage         | > 80%            | stories_with_tests / total × 100 |
| H3 | Automation coverage    | > 70%            | automated / total × 100          |
| H4 | Defect density         | < 0.30 per story | 0.30 / actual (if > 0)           |
| H5 | Performance benchmarks | Pass             | binary (100 or 0, or 100 if N/A) |

`high_priority_score = avg(normalized H1–H5)`

---

## Phase 4 — Medium criteria (15% weight)

| #  | Criterion               | Target                                                   |
|----|-------------------------|----------------------------------------------------------|
| M1 | Medium bugs resolved    | (resolved medium bugs / total medium bugs) × 100         |
| M2 | Regression tests passed | (passed regression tests / total regression tests) × 100 |
| M3 | Documentation complete  | (complete docs / required docs) × 100                    |

`medium_priority_score = avg(M1, M2, M3)`

---

## Phase 5 — Optional criteria (5% weight)

| #  | Criterion                  | Target                           |
|----|----------------------------|----------------------------------|
| O1 | Low priority bugs resolved | (resolved low / total low) × 100 |
| O2 | Code coverage              | actual / 80% (capped at 100%)    |

`optional_score = avg(O1, O2)` — if data unavailable, score = 80% (neutral)

---

## Phase 6 — Calculate readiness and generate recommendation

Use `references/metrics-formulas.md` for the readiness score formula, worked example, and benchmark interpretation.

```
readiness = critical_score×0.50 + high_priority×0.30 + medium_priority×0.15 + optional_score×0.05
```

Map score to recommendation (see thresholds above).

**Identify risks for GO-with-caveats or Conditional GO**:
- Which specific criteria failed or are below target?
- What is the consequence if released anyway?
- What acceptance must be documented?

---

## Phase 7 — Write release readiness report

Read `references/release-readiness-template.md` for the complete report structure before writing.

Write `release-readiness.md` with:

**Header + decision callout**:
```
RELEASE: {name}     DATE: {date}     DECISION: ✅ GO / 🔴 NO-GO
READINESS SCORE: XX%
```

**Executive summary** (3–5 sentences): overall health, key strengths, key gaps, decision rationale.

**Readiness scorecard**:

| Category          | Weight   | Score | Weighted |
|-------------------|----------|-------|----------|
| Critical criteria | 50%      | X%    | X%       |
| High priority     | 30%      | X%    | X%       |
| Medium priority   | 15%      | X%    | X%       |
| Optional          | 5%       | X%    | X%       |
| **Total**         | **100%** |       | **X%**   |

**Detailed criteria checklist**: all 11 criteria with actual values vs. targets and Pass/FAIL/N/A

**Open issues**:
- Open Critical bugs (if any): list with keys and summaries
- Open High bugs (if any): list with waiver status
- Failed test cases: list with keys

**Risk summary**: for Conditional GO — list accepted risks with owner and mitigation

**Sign-off section** (for Conditional GO and GO with caveats):

| Role            | Name | Decision   | Date |
|-----------------|------|------------|------|
| QA Lead         |      | ☐ Approved |      |
| Product Owner   |      | ☐ Approved |      |
| Release Manager |      | ☐ Approved |      |

**Next steps**: what must happen before deployment (e.g., "deploy migration script before app"), post-release monitoring plan.

---

## Gotchas

- If critical_score = 0%, declare NO-GO immediately and stop computing other scores — don't soften this
- "N/A" for performance or security tests should score 100% (not a failure) — explicitly call this out in the report
- Waived High bugs still require documented rationale and sign-off before they can be treated as passing
- Don't create a false sense of precision — a 92% score isn't objectively safer than 88%; use the narrative to explain what the numbers mean

---

## Reference files

- `references/metrics-formulas.md` — Readiness score formula and worked example
- `references/release-readiness-template.md` — Output report template
