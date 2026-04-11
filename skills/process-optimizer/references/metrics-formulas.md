# Process Metrics Formulas

## Cycle Time and Bottleneck Analysis

```
# Stage cycle time
stage_cycle_time = avg(time_left_stage - time_entered_stage)   # across all issues

# Bottleneck score
bottleneck_score = stage_avg_days / total_cycle_avg_days × 100

# MTTR (Mean Time To Resolve bugs)
MTTR = avg(resolution_date - created_date)   # for closed bugs

# Blocked rate
blocked_rate = blocked_issues / total_issues × 100

# Escaped defect rate
escape_rate = production_bugs / total_bugs × 100
```

**Bottleneck severity**:
| Score | Severity |
|---|---|
| > 40% | 🔴 Major bottleneck |
| 30–40% | 🟠 Moderate |
| 20–30% | 🟡 Minor |
| < 20% | ✅ Normal |

## Risk Scoring

```
risk_score = impact_score × probability_score

Impact:      Critical=5, High=4, Medium=3, Low=2, Negligible=1
Probability: Very High=5, High=4, Medium=3, Low=2, Very Low=1

Priority:
  Critical: score ≥ 20
  High:     score 15–19
  Medium:   score 9–14
  Low:      score < 9

Overall risk level = avg(risk_scores across all risks)
  High:   > 15
  Medium: 9–15
  Low:    < 9
```

## Quality Benchmarks

| Metric                     | Excellent | Good      | Acceptable | Poor   |
|----------------------------|-----------|-----------|------------|--------|
| Defect density (per story) | < 0.10    | 0.10–0.30 | 0.30–0.50  | > 0.50 |
| Test coverage              | > 95%     | 85–95%    | 70–85%     | < 70%  |
| Pass rate                  | > 98%     | 95–98%    | 90–95%     | < 90%  |
| Automation                 | > 80%     | 60–80%    | 40–60%     | < 40%  |
| DRE                        | > 95%     | 90–95%    | 85–90%     | < 85%  |

## DORA Benchmarks

| Metric                | Elite        | High    | Medium       | Low       |
|-----------------------|--------------|---------|--------------|-----------|
| Lead time for changes | < 1 hour     | < 1 day | 1 day–1 week | > 1 week  |
| Deployment frequency  | Multiple/day | Weekly  | Monthly      | Quarterly |
| MTTR                  | < 1 hour     | < 1 day | < 1 week     | > 1 week  |
| Change failure rate   | < 5%         | 5–10%   | 10–15%       | > 15%     |

## Process Improvement Metrics

```
# Velocity (reduction targets)
cycle_time_reduction = (baseline_days - current_days) / baseline_days × 100
defect_prevention_rate = defects_found_in_test / total_defects × 100
rework_reduction = (baseline_rework_hours - current_rework_hours) / baseline × 100
```
