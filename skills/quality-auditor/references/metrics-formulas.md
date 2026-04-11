# Metrics Formulas Reference

## Defect Density

```
# Per story (primary measure)
defect_density = total_bugs / total_stories

# Per story point
defect_density_sp = total_bugs / total_story_points

# Weighted (severity-adjusted)
weighted_density = (Critical×10 + High×5 + Medium×2 + Low×1) / total_stories

# Trend vs prior period
trend_pct = (current - previous) / previous × 100
```

**Quality ratings (per story)**:
| Range | Rating |
|---|---|
| < 0.10 | ✅ Excellent |
| 0.10–0.30 | 🟢 Good |
| 0.30–0.50 | 🟡 Acceptable |
| 0.50–1.00 | 🟠 Poor |
| > 1.00 | 🔴 Critical |

**Weighted density ratings**:
| Range | Rating |
|---|---|
| < 1.0 | Excellent |
| 1.0–3.0 | Good |
| 3.0–5.0 | Acceptable |
| > 5.0 | Poor |

---

## Test Coverage

```
# Execution coverage
execution_coverage = executed_tests / total_tests × 100

# Story/requirement coverage
story_coverage = stories_with_tests / total_stories × 100

# Pass rate
pass_rate = passed_tests / executed_tests × 100

# Automation ratio
automation_ratio = automated_tests / total_tests × 100

# Defect Removal Efficiency
DRE = pre_release_bugs / total_bugs × 100

# Escaped defect rate
escape_rate = production_bugs / total_bugs × 100
```

**Industry benchmarks**:
| Metric | Excellent | Good | Acceptable | Poor |
|---|---|---|---|---|
| Story coverage | > 95% | 85–95% | 70–85% | < 70% |
| Pass rate | > 98% | 95–98% | 90–95% | < 90% |
| Automation ratio | > 80% | 60–80% | 40–60% | < 40% |
| DRE | > 95% | 90–95% | 85–90% | < 85% |
| Escape rate | < 5% | 5–10% | 10–15% | > 15% |

---

## Bottleneck Analysis

```
# Bottleneck score per stage
bottleneck_score = stage_avg_days / total_cycle_days × 100

# MTTR (Mean Time To Resolve bugs)
MTTR = avg(resolution_date - created_date) for closed bugs

# Blocked rate
blocked_rate = blocked_issues / total_issues × 100
```

**Bottleneck severity**:
| Score | Severity |
|---|---|
| > 40% | 🔴 Major bottleneck |
| 30–40% | 🟠 Moderate |
| 20–30% | 🟡 Minor |
| < 20% | ✅ Normal |

**MTTR targets by priority**:
| Priority | Target |
|---|---|
| Critical | < 1 day |
| High | < 3 days |
| Medium | < 7 days |
| Low | < 14 days |

---

## Release Readiness Score

```
readiness = (
    critical_score   × 0.50 +
    high_priority    × 0.30 +
    medium_priority  × 0.15 +
    optional_score   × 0.05
)
```

**Decision thresholds**: > 95% GO | 90–95% GO with caveats | 85–90% Conditional GO | < 85% NO-GO

---

## Automation Maturity Score

```
maturity = (
    coverage_score    × 0.25 +
    cicd_score        × 0.20 +
    stability_score   × 0.20 +
    maintenance_score × 0.15 +
    reporting_score   × 0.10 +
    data_mgmt_score   × 0.10
)
```

**Maturity levels**: 0.0–1.0 Initial | 1.0–2.0 Developing | 2.0–3.0 Defined | 3.0–4.0 Managed | 4.0–5.0 Optimized

---

## Automation ROI

```
# Year 1 costs
initial_investment = (automated_tests × 2hrs + 80hrs) × hourly_rate + 7000  # licenses + infra
annual_maintenance = (40hrs/mo × 12 × hourly_rate) + 7000

# Time savings
time_saved_per_run = (total_tests × 0.25hr) - (automated_tests × 0.01hr)
annual_hours_saved  = time_saved_per_run × 20_runs × 12_months
time_savings_value  = annual_hours_saved × (hourly_rate × 0.75)

# Quality benefits
defect_prevention   = max(10, automated_tests/20) × 2500
release_acceleration = 4_releases × 2_days × 8hrs × hourly_rate
total_benefits      = time_savings_value + defect_prevention + release_acceleration

# ROI
roi = (total_benefits - total_costs) / total_costs × 100
payback_months = initial_investment / ((total_benefits - annual_maintenance) / 12)
```

**ROI benchmarks**:
| Range | Rating |
|---|---|
| > 500% | ✅ Exceptional |
| 300–500% | 🟢 Excellent |
| 150–300% | 🟡 Good |
| < 150% | 🔴 Reconsider |

---

## DORA Benchmarks (Process)

| Metric                | Elite        | High    | Medium   | Low       |
|-----------------------|--------------|---------|----------|-----------|
| Lead time for changes | < 1 hour     | < 1 day | 1d–1wk   | > 1wk     |
| Deployment frequency  | Multiple/day | Weekly  | Monthly  | Quarterly |
| MTTR                  | < 1 hour     | < 1 day | < 1 week | > 1 week  |
| Change failure rate   | < 5%         | 5–10%   | 10–15%   | > 15%     |
