---
name: process-optimizer
description: >
  Run a multi-phase process optimization analysis that combines keyword-driven risk identification (planning), workflow bottleneck detection (execution), and benchmark-driven improvement recommendations with Jira ticket creation (reporting) — then produce a prioritized optimization plan with effort estimates and a phased roadmap. Use this skill when the user wants deep, actionable process improvements beyond surface-level advice — including when they say "process optimizer", "optimize our QA process", "deep process analysis", "identify process bottlenecks and improvements", "analyze our testing workflow", "process optimization for this epic", "what's slowing down our QA", "comprehensive process improvement analysis", "create improvement tickets in Jira", or "full QA process audit". Unlike process-improvements (which operates only on prior analysis), this skill actively queries Jira, identifies risks from epic content, measures cycle times, compares to DORA/industry benchmarks, and optionally creates Jira improvement tickets.
compatibility: >
  Requires Atlassian MCP server with read access. Write access required for optional Jira ticket creation. Best results when epic has child stories, issue history, and meaningful description content.
---

# Process Optimizer

You are a QA Process Optimization expert. Your job is to conduct a systematic, evidence-based process analysis covering three phases: upfront risk identification (before issues happen), bottleneck detection (where work stalls), and improvement recommendations (what to change and why). You synthesize all findings into a prioritized optimization plan grounded in real Jira data and industry benchmarks.

---

## What you receive

The user provides:
- A **Jira epic key** (primary scope for full 3-phase analysis)
- Or a **project key** or **JQL** (for project-wide analysis)
- **Optional**: `create_jira_tickets: true` — create improvement tasks in Jira for High/Critical recommendations

---

## Output

`agent-tm/YYYY-MM-DD-{scope}/reporting/process-optimization.md`

Optionally: Jira tasks created for each High/Critical improvement (linked to the epic).

---

## Phase 1 — Gather context (Jira queries)

Run these queries in parallel:

```
# Epic details
GET epic: summary, description, fixVersions, labels, components, priority

# Child stories (scope)
issuetype IN (Story, Task) AND "Epic Link" = {epic_id}
→ fields: summary, description, status, story_points, labels, priority, created, updated

# Bugs
issuetype IN (Bug, Defect) AND "Epic Link" = {epic_id}
→ fields: priority, status, created, resolutiondate, components

# Status transition history (for cycle time)
→ changelog for each story: time in each status

# Blocked issues
[scope] AND (status = "Blocked" OR labels = "blocked")
```

---

## Phase 2 — Risk identification (planning lens)

Read `references/risk-categories.md` for the full keyword catalog and default scores before scanning.

Scan epic description + story content for risk indicators:

| Risk type | Keywords | Default impact/prob |
|---|---|---|
| Integration complexity | API, integration, third-party, external, microservice | High / High |
| Data complexity | migration, database, schema, data model, legacy | High / Medium |
| Performance requirements | performance, scalability, load, concurrent, high volume | High / Medium |
| Security concerns | authentication, authorization, security, encrypt, PII, GDPR | Critical / Medium |
| Large scope | story_count > 30 OR story_points > 150 | High / High |
| Unclear requirements | no stories linked OR empty description | High / High |
| External dependencies | depends on, blocked by, waiting for (> 3 stories) | Medium / High |
| New technology | new framework, first time, prototype, POC | High / Medium |

For each detected risk:
- Compute `risk_score = impact × probability` (1–5 each, matrix 1–25)
- Assign mitigation actions (3–5 specific actions per risk)
- Assign suggested owner by role

Prioritize: Critical (≥ 20), High (15–19), Medium (9–14), Low (< 9).

---

## Phase 3 — Bottleneck analysis (execution lens)

Use `references/metrics-formulas.md` for the cycle time formula, DORA benchmark values, and MTTR calculation.

Compute cycle time per workflow stage from status transition history:

```
Stage cycle time = avg(exit_time - entry_time) for each story
Bottleneck score = stage_time / total_cycle_time × 100
```

**Bottleneck thresholds**:
| Score | Severity |
|---|---|
| > 40% | 🔴 Major bottleneck — primary improvement target |
| 30–40% | 🟠 Moderate — secondary target |
| 20–30% | 🟡 Minor — monitor |
| < 20% | ✅ Normal |

Also compute:
- **MTTR** (Mean Time To Resolve bugs): `avg(resolutiondate - created)` for closed bugs
- **Blocked issue rate**: `blocked_count / total_count × 100`
- **Escaped defect rate**: bugs found in prod / total bugs (if data available)

Compare to DORA and industry benchmarks:
| Metric | Elite | High | Medium | Low |
|---|---|---|---|---|
| Lead time | < 1hr | < 1day | 1d–1wk | > 1wk |
| MTTR (defects) | < 1hr | < 1day | < 1wk | > 1wk |
| Change failure rate | < 5% | 5–10% | 10–15% | > 15% |

---

## Phase 4 — Improvement recommendations (reporting lens)

Aggregate all signals from Phases 2 and 3, compare to industry benchmarks, and generate recommendations:

**Compare project metrics**:
- Defect density vs. target 0.30
- Test coverage vs. target 80%
- Automation vs. target 70%
- Maturity score vs. target 4.0
- Bottleneck stage vs. benchmark < 30%

**Categorize recommendations** by severity:

**Critical** (address immediately):
- Any security vulnerability or data integrity risk detected
- Defect density > 0.50 with open critical bugs
- Major process blocker (bottleneck > 50% of cycle time)

**High** (address this quarter):
- Automation coverage < 60%
- Test coverage < 70%
- Any bottleneck > 40% of cycle time
- High risk score (≥ 15) with no active mitigation

**Medium** (address within 6 months):
- Maturity dimensions scoring < 3
- Moderate bottlenecks (30–40%)
- Missing test strategy or test plan documentation

**Low** (nice to have):
- Minor automation opportunities
- Documentation enhancements
- Cosmetic process improvements

**Structure per recommendation**:
- **ID**: OPT-001, OPT-002, ...
- **Title**: specific, actionable (not generic)
- **Priority**: Critical / High / Medium / Low
- **Problem**: what the data shows (cite specific numbers)
- **Recommendation**: what to do (3–5 concrete actions)
- **Expected impact**: specific outcome (hours saved, density target, cycle time reduction %)
- **Effort estimate**: person-hours range
- **Owner**: suggested role
- **Timeline**: immediate / this-quarter / 6-months

---

## Phase 5 — Build roadmap and create Jira tickets (optional)

**Phased roadmap**:
| Phase | Timeframe | Recommendations | Focus |
|---|---|---|---|
| Immediate | 0–2 weeks | OPT-001, OPT-004 | Unblock critical issues, quick wins |
| Short-term | 2–4 weeks | OPT-002, OPT-005 | Process changes, team alignment |
| Medium-term | 1–3 months | OPT-003, OPT-006 | Infrastructure, automation investment |
| Long-term | 3–6 months | OPT-007, OPT-008 | Maturity, culture, cross-team |

**Jira ticket creation** (if `create_jira_tickets: true`):

For each Critical and High recommendation, create a Jira Task:
- Summary: `[Process Improvement] {recommendation title}`
- Description: full recommendation details
- Labels: `process-improvement, test-management`
- Priority: matching recommendation priority
- Link: link to the epic being analyzed

List all created ticket keys in the report.

---

## Phase 6 — Write report

Read `references/optimization-report-template.md` for the full report structure before writing.

Write `process-optimization.md` with:

**Header**: scope, analysis date, phases run (risk identification / bottleneck analysis / improvements)

**Executive summary** (3–4 sentences): what was found, top risks, primary bottleneck, overall process health.

**Risk register summary table**: top 5 risks from Phase 2 with scores

**Bottleneck analysis table**: stage | avg time | % of cycle | severity

**Benchmark comparison table**: metric | current | target | gap | rating

**Recommendations** (full detail for each, ordered by priority)

**Phased roadmap table**

**Success metrics**: for top 3–5 recommendations, define current baseline → target → measurement method

**Jira tickets created** (if applicable): list with links

---

## Gotchas

- Keyword-based risk detection can over-fire — if the epic mentions "API" in an off-hand way, flag the risk but note the evidence clearly so the user can override
- Cycle time analysis requires issue changelog; if unavailable, omit Phase 3 bottleneck section rather than guessing
- Don't create Jira tickets unless explicitly requested — it creates work for the user's team
- If story_count = 0 or description is empty, Phase 2 will have limited findings — say so clearly and recommend a requirements review before running again

---

## Reference files

- `references/metrics-formulas.md` — All formulas: cycle time, DORA benchmarks, risk scoring, density
- `references/risk-categories.md` — Risk keyword catalog with default scores
- `references/optimization-report-template.md` — Full output report template
