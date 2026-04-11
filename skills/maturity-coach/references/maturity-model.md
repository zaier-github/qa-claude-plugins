# Automation Maturity Model

## Overview

The maturity model assesses 6 dimensions on a 0–5 scale. The weighted overall score determines the team's maturity level.

```
Maturity Score = (
    Coverage    × 0.25 +
    CI/CD       × 0.20 +
    Stability   × 0.20 +
    Maintenance × 0.15 +
    Reporting   × 0.10 +
    Data Mgmt   × 0.10
)
```

## Maturity Levels

| Score   | Level         | Description                                                                      |
|---------|---------------|----------------------------------------------------------------------------------|
| 4.0–5.0 | ✅ Optimized   | Continuous improvement with metrics-driven optimization; ML/predictive analytics |
| 3.0–4.0 | 🟢 Managed    | Measured and controlled; quantitative management; proactive practices            |
| 2.0–3.0 | 🟡 Defined    | Standardized and documented processes; consistent execution                      |
| 1.0–2.0 | 🟠 Developing | Repeatable with some documentation; ad-hoc but improving                         |
| 0.0–1.0 | 🔴 Initial    | Ad-hoc, chaotic, no formal process                                               |

**Industry distribution**: Initial 20% | Developing 30% | Defined 25% | Managed 20% | Optimized 5%

**Target for high-performing teams**: **4.0 / Managed**

---

## Dimension 1: Test Coverage (weight 25%)

| Score | Criteria         | Automation % |
|-------|------------------|--------------|
| 5     | > 80% automated  | > 80%        |
| 4     | 60–80% automated | 60–80%       |
| 3     | 40–60% automated | 40–60%       |
| 2     | 20–40% automated | 20–40%       |
| 1     | < 20% automated  | < 20%        |
| 0     | No automation    | 0%           |

**How to score**: `automation_pct = automated_tests / total_tests × 100`

**Detection**: Label "automated" on test issues, or customfield = "Automated"

---

## Dimension 2: CI/CD Integration (weight 20%)

| Score | Criteria                                           |
|-------|----------------------------------------------------|
| 5     | Deployment gating + automated rollback on failure  |
| 4     | Full pipeline integration — tests gate deployments |
| 3     | Tests run on every PR/commit                       |
| 2     | On-demand CI runs available                        |
| 1     | Scheduled nightly runs only                        |
| 0     | Manual execution only                              |

**Heuristic scoring** (from Jira data):
- `ci_indicators > 10 OR (automated_tests > 50 AND coverage > 80%)` → score 5
- `ci_indicators > 5 OR automated_tests > 20` → score 4
- `ci_indicators > 2 OR automated_tests > 10` → score 3
- `automated_tests > 5` → score 2
- `automated_tests > 0` → score 1
- else → score 0

**Detection**: Labels "ci-cd", "pipeline", "automated-tests"; component = "CI/CD"

---

## Dimension 3: Test Stability (weight 20%)

| Score | Criteria         | Flakiness Rate |
|-------|------------------|----------------|
| 5     | < 1% flakiness   | < 1%           |
| 4     | 1–3% flakiness   | 1–3%           |
| 3     | 3–5% flakiness   | 3–5%           |
| 2     | 5–10% flakiness  | 5–10%          |
| 1     | 10–20% flakiness | 10–20%         |
| 0     | > 20% flakiness  | > 20%          |

**How to score**: `flakiness_rate = flaky_tests / total_tests × 100`

**Detection**: Label "flaky", description contains "intermittent" or "flaky"

**If no tests yet**: default to score 3 ("not yet assessed")

---

## Dimension 4: Maintenance (weight 15%)

| Score | Criteria                                                                                |
|-------|-----------------------------------------------------------------------------------------|
| 5     | Self-healing tests or large well-maintained suite (> 50 tests, < 5 maintenance tickets) |
| 4     | Proactive maintenance with metrics tracking                                             |
| 3     | Regular maintenance schedule (> 5 tickets, including recent)                            |
| 2     | Reactive maintenance only                                                               |
| 1     | Ad-hoc fixes, no structured process                                                     |
| 0     | No maintenance process                                                                  |

**Detection**: Issues with label "test-maintenance", "test-refactor", "test-debt"; summary contains "test maintenance"

---

## Dimension 5: Reporting (weight 10%)

| Score | Criteria                                    |
|-------|---------------------------------------------|
| 5     | Predictive analytics with AI/ML insights    |
| 4     | Root cause analysis with trend tracking     |
| 3     | Trend analysis dashboards (historical view) |
| 2     | Test result dashboards (pass/fail per run)  |
| 1     | Basic pass/fail reports only                |
| 0     | No reporting                                |

**Heuristic**: Count test reports in scope (Confluence pages with label "test-report" or "test-results").
- > 15 reports → score 5; > 10 → score 4; > 5 → score 3; > 2 → score 2; else → score 1

---

## Dimension 6: Test Data Management (weight 10%)

| Score | Criteria                                    |
|-------|---------------------------------------------|
| 5     | Dynamic data generation + automated cleanup |
| 4     | Automated data provisioning                 |
| 3     | Data generation scripts                     |
| 2     | Shared test data repositories               |
| 1     | Manual setup or hardcoded data              |
| 0     | No strategy                                 |

**Heuristic**: Count test-data related issues/tickets.
- > 10 → score 5; > 5 → score 4; > 2 → score 3; > 0 → score 2; else → score 1

**Detection**: Label "test-data", "data-generation"; summary contains "test data"

---

## Improvement Targets Per Quarter

| Current Score | Target Next Quarter | Expected Actions                                          |
|---------------|---------------------|-----------------------------------------------------------|
| 0–1           | 2                   | Establish first automated tests; basic reporting          |
| 1–2           | 3                   | Achieve 40% automation; set up nightly CI run             |
| 2–3           | 3.5                 | Reach 60% automation; PR triggers; reduce flakiness       |
| 3–4           | 4.0                 | 70%+ automation; deployment gating; proactive maintenance |
| 4–5           | Maintain            | Optimize; introduce ML/predictive; self-healing           |

**Success milestones**:
- Score ≥ 3.0 in all dimensions: 6 months
- Overall score ≥ 4.0: 12 months
- Rate of improvement: 0.5 points/quarter is realistic
