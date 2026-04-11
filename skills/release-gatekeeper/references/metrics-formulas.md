# Release Readiness Formulas

## Readiness Score

```
readiness = (critical_score × 0.50) + (high_priority × 0.30) + (medium_priority × 0.15) + (optional × 0.05)
```

**Decision thresholds**:

| Score  | Decision           |
|--------|--------------------|
| > 95%  | ✅ GO               | 
| 90–95% | 🟢 GO with caveats |
| 85–90% | 🟡 Conditional GO  |
| < 85%  | 🔴 NO-GO           |

## Critical Criteria (50% — binary)

All must pass for 100%. Any failure → 0% → immediate NO-GO.

| Criterion                   | Pass condition                                      |
|-----------------------------|-----------------------------------------------------|
| Zero open critical bugs     | open_critical_count == 0                            |
| Zero high-priority blockers | open_high_count == 0 (or all waived)                |
| Core functionality tested   | all P1 tests executed and passed                    |
| Security tests passed       | all security tests passed (or N/A → counts as pass) |

## High Priority Criteria (30%)

Normalized: `score_i = min(100%, actual_i / target_i × 100)`.  
For defect density (lower = better): `score = min(100%, 0.30 / actual × 100)`.

| Criterion              | Target     |
|------------------------|------------|
| Test pass rate         | > 95%      |
| Story coverage         | > 80%      |
| Automation coverage    | > 70%      |
| Defect density         | < 0.30     |
| Performance benchmarks | Pass / N/A |

`high_priority_score = avg(5 normalized scores)`

## Medium Criteria (15%)

| Criterion               | Formula                                    |
|-------------------------|--------------------------------------------|
| Medium bugs resolved    | resolved_medium / total_medium × 100       |
| Regression tests passed | passed_regression / total_regression × 100 |
| Documentation complete  | complete_docs / required_docs × 100        |

## Optional Criteria (5%)

Default to 80% if data unavailable (neutral).

| Criterion                  | Formula                        |
|----------------------------|--------------------------------|
| Low priority bugs resolved | resolved_low / total_low × 100 |
| Code coverage              | min(100%, actual / 80 × 100)   |

## Worked Example

```
Critical: all pass = 100% × 0.50 = 50.00%

High: pass rate 97%, coverage 85%, automation 72%, density 0.24, perf N/A
  = avg(100%, 100%, 100%, 100%, 100%) = 100% × 0.30 = 30.00%

Medium: bugs 90%, regression 98%, docs 85%
  = avg = 91% × 0.15 = 13.65%

Optional: low bugs 70%, code cov 75%→94%
  = avg = 82% × 0.05 = 4.10%

Total = 97.75% → ✅ GO
```
