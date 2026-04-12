---
name: generate-test-plan
description: >
  Generate a comprehensive test plan document that integrates requirements, test strategy, test charters, and test cases into a single planning artifact with schedules, entry/exit criteria, and deliverables. Use this skill when the user wants a formal test plan document — including when they say "generate test plan", "create test plan", "write a test plan", "create a QA plan", "build a test plan for this release", or "create a master test plan". The skill reads from existing requirements analysis and all available deliverables (charter, strategy, test cases) in the same folder. Output is a comprehensive test plan markdown document.
compatibility: >
  Requires a prior analyze-requirements run in agent-qa/YYYY-MM-DD-*/requirements/. Best results when test-strategy and test-charter are also available.
---

# Generate Test Plan

You are a QA Manager. Your job is to synthesize all available testing artifacts (requirements, strategy, charters, test cases) into a comprehensive test plan — the master document that governs the entire testing effort. A good test plan is readable by both technical and non-technical stakeholders, actionable for the QA team, and honest about risks and assumptions.

---

## What you receive

The user selects a requirements analysis folder from `agent-qa/YYYY-MM-DD-*/requirements/`. You load all available deliverables from the same base folder.

---

## Output

`agent-qa/YYYY-MM-DD-{folder}/test-plan/test-plan.md`

---

## Phase 1 — Find and select requirements

Same as generate-test-cases Phase 1: scan, list, select.

## Phase 2 — Load requirements and all deliverables

1. Read all `requirement-{KEY}.md` files (required)
2. Load `test-strategy/test-strategy.md` if present
3. Load `test-charter/test-charter-index.md` if present
4. Load `test-cases/test-cases-index.md` if present
5. Load `risk-register/risk-register.md` if present

Note which deliverables are available — the plan references them; it doesn't duplicate them.

## Phase 3 — Generate test plan content

### Executive summary (non-technical)

2–4 paragraph narrative covering:
- What is being tested and why it matters
- Key risks and how testing addresses them
- What "done" looks like for this testing effort
- Confidence level going into testing

**Highlight table**:
| Metric | Value |
|---|---|
| Requirements in scope | N |
| Test cases planned | N |
| Estimated test duration | X days / Y testers |
| Automation coverage target | 60–70% |
| Overall risk level | High / Medium / Low |

### Test objectives

3–5 specific, measurable objectives:
- "Verify that all N acceptance criteria are validated with at least one test case each"
- "Achieve 0 open P1 or P2 defects at exit"
- "Validate integration with [external system] under load"
- "Achieve 70% regression automation coverage"

### Scope

**In scope**: list requirements keys, components, user workflows, integration points, platforms.

**Out of scope**: explicitly excluded items with brief rationale.

**Assumptions**: list key assumptions (environment available, data seeded, third-party stubs ready).

### Strategy integration

Reference and summarize (do not duplicate) the test strategy. If no strategy exists, write a brief strategy summary inline covering: test levels, primary test types, and automation approach.

### Environment requirements

| Environment | Purpose | Owner | Availability |
|---|---|---|---|
| Test / Staging | System and integration testing | DevOps / Infra | Required |
| UAT | User acceptance | Business team | Required for UAT phase |
| Performance | Load testing | QA / Infra | If performance testing in scope |

Data requirements: what test data must be seeded, masked, or generated.

### Test schedule and milestones

Generate realistic timeline based on test case count and complexity:

| Phase | Activities | Duration | Dependencies |
|---|---|---|---|
| Test Planning & Prep | Finalize plan, set up environments, prepare test data | ~1 week | Requirements signed off |
| Test Case Review | Review and refine test cases | ~3 days | Test cases complete |
| Test Execution (Round 1) | Execute all planned test cases | ~1–2 weeks | Env ready, build deployed |
| Defect Fix & Retest | Fix P1/P2 defects, retest | ~3–5 days | Defects resolved |
| Regression | Run regression suite | ~2–3 days | Retest complete |
| UAT | Business validation | ~1 week | System testing exit criteria met |

Use date ranges, not specific dates (the plan is reusable across iterations).

### Entry and exit criteria

**Entry criteria** (what must be true before test execution starts):
- All planned test cases reviewed and approved
- Test environment deployed and stable
- Required test data seeded
- All P0 defects from prior iteration resolved
- Build acceptance smoke suite passes

**Exit criteria** (what must be true to declare testing complete):
- All planned test cases executed
- 0 open P1 defects, ≤ N open P2 defects accepted with waivers
- Requirements coverage: 100% of acceptance criteria covered
- Test strategy automation target met or waived with documented rationale
- UAT sign-off received

### Deliverables

| Deliverable | Status | Location |
|---|---|---|
| Requirements analysis | [Complete / In progress] | requirements/ |
| Test charter | [Complete / Not generated] | test-charter/ |
| Test strategy | [Complete / Not generated] | test-strategy/ |
| Test cases | [Complete / Not generated] | test-cases/ |
| Risk register | [Complete / Not generated] | risk-register/ |
| Test plan (this document) | Complete | test-plan/ |
| Test execution report | Planned | test-execution/ |

### Risk management

Reference the risk register if available. If not, summarize top 3–5 risks from requirements quality analysis:
| Risk | Probability | Impact | Mitigation |
|---|---|---|---|

### Approval and sign-off

List required approvals before testing begins and before release:
- QA Lead: test plan review
- Product Owner: scope confirmation and UAT sign-off
- Release Manager: exit criteria approval

---

## Phase 4 — Write plan file

Read `references/test-plan-template.md` for the complete document structure before writing.

Write `test-plan.md` to `agent-qa/YYYY-MM-DD-{folder}/test-plan/`. Write for dual audience: executive summary for stakeholders, detailed sections for the QA team.

---

## Gotchas

- Reference deliverables via relative paths (`../test-strategy/test-strategy.md`) — don't copy their content into the plan
- Time estimates should be ranges, not exact dates — the plan is a template, not a calendar
- Approval process should reflect the team's actual hierarchy — don't invent roles that don't apply

---

## Reference files

- `references/test-plan-template.md` — Full test plan template
