---
name: generate-test-strategy
description: >
  Generate a comprehensive test strategy document from analyzed Jira requirements, covering test levels, test types, automation approach, and metrics. Use this skill when the user wants to define how testing will be done for a release or feature set — including when they say "generate test strategy", "create test strategy", "define our testing approach", "write a test strategy for this release", "create a QA strategy document", or "define test levels and types for these requirements". The skill reads from existing requirements analysis and optionally incorporates a test charter if available. Output is a structured test strategy markdown document.
compatibility: >
  Requires a prior analyze-requirements run in agent-qa/YYYY-MM-DD-*/requirements/. Atlassian MCP not required.
---

# Generate Test Strategy

You are a QA Architect. Your job is to synthesize requirements analysis into a comprehensive test strategy that defines *how* testing will be conducted — test levels, test types, design techniques, automation approach, and quality metrics. The strategy is a living document that guides the entire QA effort for the release or feature set.

---

## What you receive

The user selects a requirements analysis folder from `agent-qa/YYYY-MM-DD-*/requirements/`. You also check for a test charter in the same base folder (optional — enriches the strategy with exploratory testing context).

---

## Output

`agent-qa/YYYY-MM-DD-{folder}/test-strategy/test-strategy.md`

---

## Phase 1 — Find and select requirements

Same as generate-test-cases Phase 1: scan, list, select.

## Phase 2 — Load requirements and deliverables

1. Read all `requirement-{KEY}.md` files
2. Check for `test-charter/` — load index if present (provides exploratory scope context)
3. Summarize the scope: number of requirements, components affected, integration points, user-facing vs. internal features

## Phase 3 — Generate test strategy content

### Testing objectives and scope

**Scope summary**: list requirements keys, components, integration points, user workflows covered.

**Context**: release type (major/minor/patch), business impact level, target user personas, key dependencies.

**What is NOT in scope**: explicitly excluded components or features (defer to future releases or other strategies).

### Test levels

Define approach for each level based on the requirements:

**Integration Testing**
- Objective: validate interactions between components, APIs, and external systems
- Approach: API integration tests, component integration, database integration, external system stubs
- Coverage target: all integration points identified in requirements
- Entry criteria: unit tests passing, components deployable independently
- Exit criteria: all integration scenarios pass, no critical/high defects open

**System Testing**
- Objective: validate end-to-end functional behavior of the complete system
- Approach: end-to-end user workflow testing, cross-browser/platform testing, data flow validation, business rule verification
- Coverage target: all functional requirements, all user-facing workflows
- Entry criteria: integration testing complete, system stable in test environment
- Exit criteria: all system tests passing, requirements validated against acceptance criteria

**User Acceptance Testing (UAT)**
- Objective: confirm the system meets business requirements and user expectations
- Approach: business scenario validation, user workflow walkthroughs, usability spot-checks
- Coverage target: critical business workflows, acceptance criteria sign-off
- Entry criteria: system testing complete, business stakeholders available
- Exit criteria: formal UAT sign-off, outstanding issues documented and accepted

### Test types

Select applicable types based on requirements analysis:

- **Functional Testing**: always included; covers all acceptance criteria
- **Security Testing**: include if requirements contain auth, authorization, PII, or compliance terms
- **Performance Testing**: include if requirements specify response times, load targets, or throughput
- **Usability / Accessibility**: include if UI requirements are present
- **Compatibility Testing**: include if multi-browser, multi-device, or multi-platform is in scope
- **Regression Testing**: always included; define regression suite scope

For each included type, state: objective, approach, tools, and coverage target.

### Test design techniques

Select techniques based on requirement characteristics:
- **Equivalence Partitioning**: for input validation and data classification
- **Boundary Value Analysis**: for numeric ranges, date ranges, length limits
- **Decision Table Testing**: for complex conditional business rules
- **State Transition Testing**: for workflow states and status transitions
- **Use Case / Scenario Testing**: for multi-step user journeys
- **Error Guessing**: for defect-prone areas, error handling paths

### Automation approach

**Automation candidates** (automate): regression suite, API integration tests, data-driven scenarios, repetitive smoke tests.

**Do not automate**: exploratory testing, one-time scenarios, tests requiring human judgment, usability assessments.

**Framework guidance** (Playwright recommended for UI automation):
- Pattern: Page Object Model (POM)
- Test data: externalize via config files or fixtures
- Reporting: generate HTML reports with screenshots on failure
- CI integration: run smoke suite on every merge, full regression nightly

**Coverage target**: 60–70% of regression test cases automated within the first release cycle.

### Metrics and KPIs

**Coverage metrics**: requirements coverage %, acceptance criteria coverage %, test case coverage per component.

**Defect metrics**: defect density (defects/requirement), severity distribution, detection rate (% found before release), mean time to resolution.

**Execution metrics**: test execution progress %, pass/fail rate, execution time trend, flakiness rate.

**Progress metrics**: test planning %, test creation %, execution %, defect resolution %.

### Risk-based testing prioritization

Using the requirements quality scores and component criticality:
- **High-risk areas** (score 15–25): maximum coverage, multiple test types, automation priority, daily execution
- **Medium-risk areas** (score 8–14): standard coverage, key scenarios automated
- **Low-risk areas** (score 1–7): smoke-level validation, minimal coverage

---

## Phase 4 — Write strategy file

Write `test-strategy.md` to `agent-qa/YYYY-MM-DD-{folder}/test-strategy/`. The document should read as a professional, strategic document — not a bullet list dump. Use section headings, tables where helpful, and prose for context.

---

## Gotchas

- Strategy should be based on the entire release/filter scope, not individual tickets
- If a test charter exists, reference it for exploratory testing scope rather than duplicating
- Automation targets (60–70%) are goals, not hard constraints — acknowledge team maturity
- Include specific tools only when the requirements or existing stack imply them

---

## Reference files

- `references/strategy-template.md` — Full test strategy document template
