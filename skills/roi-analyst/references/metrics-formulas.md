# ROI and Automation Metrics Formulas

> **See also**: `quality-auditor/references/metrics-formulas.md` — the most complete metrics reference in the suite, covering defect density, automation ratio targets, and quality benchmarks referenced in the ROI model.

## ROI Calculation

```
# Development investment
dev_hours          = automated_tests × 2        # 2 hrs/test (E2E average)
framework_setup    = 80                          # hours, one-time
initial_investment = (dev_hours + 80) × rate + 5000 + 2000  # licenses + infra

# Annual maintenance
annual_maintenance = (40 × 12 × rate) + 5000 + 2000

# Year 1 costs
total_year1_costs  = initial_investment + annual_maintenance

# Time savings
manual_mins_per_test    = 15    # default
automated_mins_per_test = 0.6   # default
runs_per_month          = 20    # default

time_saved_per_run = (total_tests × 15/60) - (automated_tests × 0.6/60)   # hours
annual_hours_saved = time_saved_per_run × runs_per_month × 12
time_savings_value = annual_hours_saved × (rate × 0.75)   # QA rate = 75% billing

# Quality benefits
defects_prevented       = max(10, automated_tests / 20)
defect_prevention_value = defects_prevented × 2500
release_time_value      = 4 × 2 × 8 × rate   # 4 releases × 2 days × 8hrs
quality_benefits        = defect_prevention_value + release_time_value

# ROI
total_year1_benefits = time_savings_value + quality_benefits
net_savings          = total_year1_benefits - total_year1_costs
roi_pct              = (net_savings / total_year1_costs) × 100
payback_months       = initial_investment / ((total_year1_benefits - annual_maintenance) / 12)

# 3-year projection
year2_benefits = total_year1_benefits × 1.10
year3_benefits = total_year1_benefits × 1.20
roi_3year      = ((total + year2 + year3 benefits - costs) / costs) × 100
```

## Industry Benchmarks

| Metric              | Exceptional | Excellent  | Good        | Reconsider  |
|---------------------|-------------|------------|-------------|-------------|
| ROI Year 1          | > 500%      | 300–500%   | 150–300%    | < 150%      |
| Payback             | < 3 months  | 3–6 months | 6–12 months | > 12 months |
| Automation coverage | > 80%       | 60–80%     | 40–60%      | < 40%       |

## Automation Efficiency

```
automation_efficiency = (time_saved_per_run / maintenance_hours_monthly) × 100
dev_efficiency        = automated_tests / (dev_hours + framework_setup)   # tests/hour
```

Benchmarks: 0.5–1.0 tests/hour for E2E | 1–3 tests/hour for API tests
