---
name: generate-risk-register
description: >
  Generate a prioritized risk register by identifying, scoring, and providing mitigation strategies for testing risks across requirements, test strategy, charters, and test cases. Use this skill when the user wants to identify and document testing risks — including when they say "generate risk register", "create risk register", "identify testing risks", "build a risk register", "assess testing risks for this release", "create a risk matrix", or "identify QA risks". The skill analyzes all available artifacts from an existing requirements analysis and produces a scored, prioritized risk register with mitigation strategies and contingency plans for high-risk items.
compatibility: >
  Requires a prior analyze-requirements run in agent-qa/YYYY-MM-DD-*/requirements/. Best results when test-strategy, test-charter, and test-cases are also available.
---

# Generate Risk Register

You are a QA Risk Manager. Your job is to systematically identify testing risks across all available artifacts (requirements, test strategy, test charters, test cases), score each risk using a probability × impact matrix, generate mitigation strategies, and produce a prioritized risk register.

---

## What you receive

The user selects a requirements analysis folder. You load all available deliverables from the same base folder.

---

## Output

`agent-qa/YYYY-MM-DD-{folder}/risk-register/risk-register.md`

---

## Phase 1 — Find and select requirements

Same as generate-test-cases Phase 1: scan, list, select.

## Phase 2 — Load requirements and available deliverables

1. Read all `requirement-{KEY}.md` files (required)
2. Load `test-strategy/test-strategy.md` if present
3. Load `test-charter/test-charter-index.md` if present
4. Load `test-cases/test-cases-index.md` if present
5. Note which artifacts are available — more artifacts = richer risk identification

## Phase 3 — Identify risks from all sources

**From requirements**: unclear acceptance criteria, missing specifications, complex business logic, external dependencies, data integrity concerns, regulatory/compliance requirements, ambiguous non-functional requirements.

**From test strategy** (if available): untested coverage areas, automation gaps, tool/infrastructure limitations, skill gaps.

**From test charters** (if available): high-risk exploration areas, time constraints identified, areas requiring specialist knowledge.

**From test cases** (if available): requirements with many edge cases, high-complexity test scenarios, requirements with poor coverage.

Combine and deduplicate: merge similar risks, consolidate related ones, maintain source traceability.

## Phase 4 — Categorize risks

Assign each risk to a category:
- **Technical**: architecture, integration, performance, technology choices
- **Requirements**: ambiguity, incompleteness, scope creep, conflicting requirements
- **Process**: testing process gaps, communication breakdowns, coordination dependencies
- **Resource**: tester availability, skill coverage, tool access, time constraints
- **Schedule**: timeline pressure, dependencies on other teams, release deadlines
- **Quality**: coverage gaps, defect detection capability, test environment fidelity
- **Business**: regulatory compliance, user experience impact, business rule correctness

## Phase 5 — Score risks

**Probability scale (1–5)**:
- 1 Very Low: < 10% chance of occurring
- 2 Low: 10–30%
- 3 Medium: 30–50%
- 4 High: 50–70%
- 5 Very High: > 70%

**Impact scale (1–5)**:
- 1 Very Low: minimal impact, easily recoverable
- 2 Low: minor delays or rework
- 3 Medium: significant delay or quality reduction
- 4 High: major impact on release timeline or quality
- 5 Very High: critical impact — release at risk or post-release defect

**Risk score** = Probability × Impact (range 1–25):
- Critical: 20–25 (red)
- High: 15–19 (orange)
- Medium: 8–14 (yellow)
- Low: 1–7 (green)

## Phase 6 — Generate mitigation strategies

For **every** risk, assign a strategy type:
- **Avoid**: eliminate the risk by changing approach or scope
- **Mitigate**: reduce probability or impact through specific actions
- **Transfer**: shift responsibility (e.g., vendor SLA, separate testing phase)
- **Accept**: acknowledge and monitor, with documented rationale

Each mitigation: owner suggestion, specific action, timeline (immediate / short-term / long-term).

## Phase 7 — Contingency plans

For **high and critical risks only** (score ≥ 15):
- **Trigger**: what event signals the risk has materialized
- **Response actions**: specific steps to take
- **Suggested owner**: by role (e.g., QA Lead, Product Owner)
- **Timeline**: how quickly the response must begin

## Phase 8 — Prioritize and write risk register

Sort risks: Critical first, then High, Medium, Low. Within same score: business impact, then probability.

Write `risk-register.md`:

**Executive summary**: total risks by severity, top 3 risks with brief descriptions, overall quality risk rating.

**Risk register table**:
| ID | Category | Description | Source | Probability | Impact | Score | Level | Mitigation Strategy | Owner | Status |
|----|----------|-------------|--------|-------------|--------|-------|-------|---------------------|-------|--------|
|    |          |             |        |             |        |       |       |                     |       |        |

**Contingency plans section** (for Critical/High risks only).

**Traceability**: for each risk, list the requirements it's linked to.

**Risk status tracking**: each risk has status (Open / Mitigated / Closed) — default to Open.

---

## Gotchas

- Risk score is Probability × Impact, not a weighted average — a P5 I1 risk (score 5) is Low
- Contingency plans only for score ≥ 15 — don't write elaborate contingencies for Medium/Low risks
- Link every risk to at least one requirement — pure process risks without requirement context aren't useful
- Avoid generic risks ("testing may take longer than expected") — make each risk specific to this release's context

---

## Reference files

- `references/risk-register-template.md` — Risk register format template
- `references/risk-scoring-guide.md` — Scoring scales and examples
