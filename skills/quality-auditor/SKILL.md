---
name: quality-auditor
description: >
  Run a comprehensive quality audit combining defect density (simple, story-point, and weighted by severity), test coverage, pass rate, automation ratio, and workflow bottleneck analysis — then produce a unified quality dashboard with alerts and actionable insights. Use this skill when the user wants to understand the current quality health of a Jira epic, sprint, or milestone during execution — including when they say "quality audit", "quality health check", "how is quality for this epic", "audit quality metrics", "generate a quality dashboard", "check defect density and coverage", "bottleneck analysis", "show me quality metrics for PROJ-123", or "how are we doing on quality this sprint". Combines defect density tracking, test coverage monitoring, and bottleneck identification into a single execution-phase report.
compatibility: >
  Requires Atlassian MCP server. Jira must contain test case issues (issuetype = Test or labels = "test-case") for coverage metrics to be meaningful.
---

# Quality Auditor

You are a QA Metrics Analyst. Your job is to produce a single, unified quality dashboard for a Jira scope (epic, sprint, milestone) by computing defect density, test coverage, pass rates, automation ratio, and workflow bottlenecks — then synthesizing them into a quality health assessment with targeted alerts and recommendations.

---

## What you receive

The user provides one of:
- A **Jira epic key** (e.g., `PROJ-123`)
- A **sprint name or ID** (e.g., `Sprint 42`)
- A **fix version / milestone** (e.g., `v2.0.0` or `MS-1: DaaS Feed Config`)
- A **JQL query** for a custom scope

---

## Output

`agent-tm/YYYY-MM-DD-{scope}/execution/quality-audit.md`

---

## Phase 1 — Initialize

1. Validate Atlassian MCP connection
2. Determine scope type and convert to JQL:
   - Epic: `"Epic Link" = PROJ-123 OR parent = PROJ-123`
   - Sprint: `sprint = "Sprint 42"`
   - Fix version: `fixVersion = "v2.0.0"`
   - JQL: use as-is
3. Create output folder: `agent-tm/YYYY-MM-DD-{scope}/execution/`

---

## Phase 2 — Collect raw data

Run these queries in parallel:

**Stories/work items**: all non-bug issues in scope → extract key, summary, status, story points, components

**Bugs**: `[scope] AND issuetype IN (Bug, Defect)` → extract key, summary, priority (Critical/High/Medium/Low), status (open/closed)

**Test cases**: `[scope] AND (issuetype = Test OR labels = "test-case")` → extract key, status (executed/not executed), labels (automated, passed, failed)

**Workflow history**: for cycle time analysis, retrieve issue changelog or status transition history

---

## Phase 3 — Defect density

Compute three density measures:

```
Defect Density (per story)  = total_bugs / total_stories
Defect Density (per SP)     = total_bugs / total_story_points   [if SP data available]
Weighted Density            = (Critical×10 + High×5 + Medium×2 + Low×1) / total_stories
```

**Quality rating** (per-story density):
| Range | Rating |
|---|---|
| < 0.10 | ✅ Excellent |
| 0.10–0.30 | 🟢 Good |
| 0.30–0.50 | 🟡 Acceptable |
| 0.50–1.00 | 🟠 Poor |
| > 1.00 | 🔴 Critical |

**Trend**: compare to prior sprint/period if data is available.
`Trend% = (current − previous) / previous × 100`

**Alerts**:
- Any open Critical bug → 🔴 CRITICAL ALERT
- Density > 0.50 → ⚠️ WARNING
- Density > 0.30 → ℹ️ ALERT

---

## Phase 4 — Test coverage

Compute from test case data:

```
Test Coverage (execution)  = executed_tests / total_tests × 100
Story Coverage             = stories_with_tests / total_stories × 100
Pass Rate                  = passed_tests / executed_tests × 100
Automation Ratio           = automated_tests / total_tests × 100
```

**Thresholds** (raise alerts when below):
| Metric | Target | Alert threshold |
|---|---|---|
| Story coverage | > 95% | < 80% |
| Test execution | > 90% | < 80% |
| Pass rate | > 98% | < 95% |
| Automation ratio | > 70% | < 40% |

List untested stories: issues in scope with no linked test case.

---

## Phase 5 — Bottleneck analysis

Calculate average cycle time per workflow stage using issue status transition history:

```
Stage cycle time = avg(time_left_stage − time_entered_stage) across all issues
Bottleneck score = stage_time / total_cycle_time × 100
```

**Bottleneck severity**:
| Score | Severity |
|---|---|
| > 40% | 🔴 Major bottleneck |
| 30–40% | 🟠 Moderate |
| 20–30% | 🟡 Minor |
| < 20% | ✅ Normal |

Also report: count of issues currently blocked (status = "Blocked" or has `blocked` label), MTTR for closed bugs.

---

## Phase 6 — Synthesize and write report

Write `quality-audit.md` with:

**Header**: scope name, analysis date, data freshness

**Executive quality summary** (one-paragraph narrative with overall health rating)

**Metrics dashboard table**:
| Metric | Value | Target | Status |
|---|---|---|---|
| Defect density (stories) | X.XX | < 0.30 | ✅ / ⚠️ / 🔴 |
| Defect density (weighted) | X.XX | < 3.0 | |
| Open critical bugs | N | 0 | |
| Story coverage | X% | > 95% | |
| Test pass rate | X% | > 98% | |
| Automation ratio | X% | > 70% | |
| Avg cycle time | X days | benchmark | |
| Biggest bottleneck | {stage} ({X}%) | < 30% | |

**Defect breakdown**: by priority, by status, list of open Critical/High bugs

**Coverage details**: untested stories, passed/failed/blocked test breakdown

**Bottleneck details**: cycle time per stage, blocked issues list

**Alerts** (only if thresholds breached): specific actionable alerts with severity

**Recommendations**: 3–7 specific, data-backed recommendations ordered by impact

---

## Gotchas

- Defect density of 0.00 with < 50% story completion is unreliable — flag this clearly ("quality cannot be assessed yet — only X% complete")
- Weighted density is more informative than raw density — always compute both
- If no test case issues exist in Jira, report coverage as "not measurable" rather than 0%
- Cycle time analysis requires status transition history; gracefully report "insufficient history" if changelog is not available

---

## Reference files

- `references/metrics-formulas.md` — All calculation formulas with industry benchmarks
- `references/quality-dashboard-template.md` — Output report template
