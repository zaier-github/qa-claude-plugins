# Risk Scoring Guide

## Probability scale (1–5)

| Score | Label     | Likelihood | Example                                     |
|-------|-----------|------------|---------------------------------------------|
| 1     | Very Low  | < 10%      | Theoretical edge case with no precedent     |
| 2     | Low       | 10–30%     | Has happened before but rarely              |
| 3     | Medium    | 30–50%     | Reasonably likely given the complexity      |
| 4     | High      | 50–70%     | Likely given current team/environment state |
| 5     | Very High | > 70%      | Expected based on past patterns             |

## Impact scale (1–5)

| Score | Label     | Consequence                                                              |
|-------|-----------|--------------------------------------------------------------------------|
| 1     | Very Low  | Minimal — isolated issue, easily fixed post-release                      |
| 2     | Low       | Minor delay or rework; users can work around it                          |
| 3     | Medium    | Significant delay, visible defect, or moderate rework                    |
| 4     | High      | Major release delay, user-facing regression, business impact             |
| 5     | Very High | Release blocked, data corruption, security breach, or compliance failure |

## Risk score matrix

|                   | Impact 1 | Impact 2 | Impact 3 | Impact 4 | Impact 5 |
|-------------------|----------|----------|----------|----------|----------|
| **Probability 5** | 5 🟢     | 10 🟡    | 15 🟠    | 20 🔴    | 25 🔴    |
| **Probability 4** | 4 🟢     | 8 🟡     | 12 🟡    | 16 🟠    | 20 🔴    |
| **Probability 3** | 3 🟢     | 6 🟢     | 9 🟡     | 12 🟡    | 15 🟠    |
| **Probability 2** | 2 🟢     | 4 🟢     | 6 🟢     | 8 🟡     | 10 🟡    |
| **Probability 1** | 1 🟢     | 2 🟢     | 3 🟢     | 4 🟢     | 5 🟢     |

**Levels**:
- 🔴 **Critical**: 20–25 — Immediate escalation and contingency plan required
- 🟠 **High**: 15–19 — Contingency plan required; monitor closely
- 🟡 **Medium**: 8–14 — Active mitigation; review weekly
- 🟢 **Low**: 1–7 — Monitor; review at sprint close

## Mitigation strategy types

| Type         | When to use                                                                     |
|--------------|---------------------------------------------------------------------------------|
| **Avoid**    | Risk can be eliminated by changing scope, design, or approach                   |
| **Mitigate** | Risk probability or impact can be reduced through specific actions              |
| **Transfer** | Risk responsibility can be shifted (vendor SLA, insurance, separate test phase) |
| **Accept**   | Risk is understood, cost of mitigation exceeds benefit; document the decision   |

## Common risk identification patterns

**Requirements risks**:
- Acceptance criteria missing or vague → Requirements risk, Probability 4, Impact 3–4
- Requirement references external system without SLA → Technical + Schedule risk

**Technical risks**:
- New technology or framework with no team experience → Technical, Probability 3–4
- Shared module changed by many tickets → Technical, high impact

**Process risks**:
- No test automation in place for regression → Quality, Probability 4 (regression will take long), Impact 3
- No QA environment until late in sprint → Schedule + Quality

**Resource risks**:
- Single tester covering large scope → Resource, Probability 3, Impact 4
