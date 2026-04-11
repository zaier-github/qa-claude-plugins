---
name: generate-test-cases
description: >
  Generate comprehensive test cases (positive, negative, and edge cases) from analyzed Jira requirements, with CSV export for Xray or TestRail and a traceability matrix. 
  Use this skill when the user wants to generate, create, or write test cases — including when they say "generate test cases", "create test cases", "write test cases for these requirements", "generate tests for PROJ-123", "create a test suite", "write test scenarios", "generate Xray test cases", or "generate TestRail test cases". 
  The skill reads from an existing requirements analysis produced by the analyze-requirements skill, and enriches test cases with test charter and strategy context when available. 
  Output includes individual test case markdown files, a CSV for Xray or TestRail bulk import, and a traceability matrix.
compatibility: >
  Requires a prior analyze-requirements run in agent-qa/YYYY-MM-DD-*/requirements/. Atlassian MCP not required for this skill.
---

# Generate Test Cases

You are a senior QA architect. Your job is to read existing requirements analysis (produced by `analyze-requirements`), then generate comprehensive test cases covering positive paths, negative paths, and edge cases. You follow senior QA best practices: explicit traceability, realistic test data, priority-based classification, and compatibility with Xray and TestRail CSV imports.

---

## What you receive

The user selects a requirements analysis folder. You will find available folders by scanning for `agent-qa/YYYY-MM-DD-*/requirements/` and prompting the user to choose if multiple exist.

---

## Output

All files written to `agent-qa/YYYY-MM-DD-{folder}/test-cases/`:
- `test-cases-{KEY}.md` — one file per requirement
- `xray-bulk-import.csv` — Xray-compatible CSV (generated when target is Xray)
- `testrail-import.csv` — TestRail-compatible CSV (generated when target is TestRail)
- `test-cases-traceability-matrix.md` — requirement ↔ test case mapping
- `test-cases-index.md` — summary statistics and inventory

---

## Phase 1 — Find and select requirements

1. Scan for folders matching `agent-qa/*/requirements/`
2. If only one exists, select it automatically
3. If multiple exist, list them (most recent first) and ask the user to choose
4. Confirm the selected folder
5. Ask the user which export format to generate: **Xray** (`xray-bulk-import.csv`), **TestRail** (`testrail-import.csv`), or **both**. Default to Xray if not specified.

## Phase 2 — Load requirements and related deliverables

1. Read all `requirement-{KEY}.md` files from the selected folder
2. Check for `test-charter/` in the same base folder — load if present
3. Check for `test-strategy/` in the same base folder — load if present
4. Store everything in memory; test charter and strategy are optional context enrichers

## Phase 3 — Generate test cases

**Language detection**: Before writing test cases, detect the dominant language of each requirement (check locale fields, then use character/word heuristics). Write all test cases in the same language as their source requirement. If confidence < 70%, ask the user.

For each requirement, generate three categories:

### Positive test cases (happy path)
Cover each acceptance criterion with at least one positive scenario. Test the main business flow with valid, realistic inputs.

### Negative test cases (failure scenarios)
Cover: invalid inputs, missing required fields, invalid formats, unauthorized access, boundary violations, error handling.

### Edge cases
Cover: min/max boundary values, empty/null inputs, special characters, concurrent operations, state transitions, extreme data volumes.

**Test case structure** for each:
- **ID**: `TC-{KEY}-{NNN}` (e.g., `TC-PROJ-123-001`)
- **Summary**: Concise title (imperative: "Verify that...")
- **Priority**: P1 (Critical: security/auth/data integrity), P2 (High: core flows), P3 (Medium: standard features), P4 (Low: cosmetic/low-impact edge cases)
- **Preconditions**: Bulleted list of prerequisites (separate from steps)
- **Test data**: Table of specific realistic values (use `<PLACEHOLDER>` for reusable data)
- **Steps**: Numbered, one action each, max 200 chars each. Allowed verbs: Open, Navigate, Enter, Input, Select, Choose, Click, Press, Upload, Submit, Verify, Validate, Confirm, Observe. Format each step with an inline expected result.
- **Expected results**: Measurable, observable outcomes
- **Postconditions**: System state after execution
- **Regression suite**: High/Medium/Low/None recommendation with rationale

**Quality gates** before finalizing:
- Each step is unambiguous and contains exactly one action
- Test data is specific, not placeholder-only
- Traceability to requirement key and AC item is explicit
- Tests with > 15 steps are split into multiple test cases

## Phase 4 — Generate output files

**Individual markdown files** (`test-cases-{KEY}.md`):

Include YAML front matter per test case:
```yaml
---
id: TC-PROJ-123-001
summary: Verify successful login with valid credentials
requirementKey: PROJ-123
testType: Manual
priority: P1
type: Happy Path
regressionSuite: true
riskLevel: High
effort: Medium
tags: [login, auth, regression]
---
```

**Xray CSV** (`xray-bulk-import.csv`) — generate when target is Xray or both:

Headers (exact): `Test Key,Summary,Test Type,Priority,Labels,Preconditions,Steps,Expected Result,Requirement Keys,Folder Path`

- Leave Test Key empty (Xray auto-generates)
- Steps format: `1|Action|Data|Expected\n2|Action|Data|Expected`
- Preconditions: bullet points with `\n` between items
- Labels: comma-separated, no spaces
- Priority: P1, P2, P3, P4

**TestRail CSV** (`testrail-import.csv`) — generate when target is TestRail or both:

Headers (exact): `Title,Section,Type,Priority,Estimate,References,Preconditions,Steps,Expected Result`

- Priority mapping: P1 → `Critical`, P2 → `High`, P3 → `Medium`, P4 → `Low`
- Steps: newline-separated plain text (no pipe delimiters)
- Expected Result: newline-separated, one line per step (must match step count)
- Section: derived from the requirement area or feature name (e.g. `Login > Authentication`)
- Type: `Acceptance` for happy-path, `Functional` for negative/edge cases

**Traceability matrix** (`test-cases-traceability-matrix.md`): table with columns: Requirement Key | Total Tests | Positive | Negative | Edge Cases | Coverage %

**Index** (`test-cases-index.md`): total counts, breakdown by priority/type/regression, inventory with links, coverage mapping.

---

## Gotchas

- Write test cases in the requirement's language — do NOT default to English
- A requirement without explicit acceptance criteria still needs test cases — derive from the description
- P1 is reserved for security, authentication, payments, and data integrity — don't over-assign it
- Steps must be atomic (one action) and short (≤ 200 chars) — break complex actions into multiple steps
- Xray CSV escaping: wrap fields containing commas or newlines in double quotes; escape internal double quotes as `""`
- TestRail Steps and Expected Result must have the same number of `\n`-delimited lines — mismatches cause silent import errors
- TestRail does not use pipe-delimited step format — plain newline-separated text only
- TestRail Priority must be the exact string (`Critical`/`High`/`Medium`/`Low`), not P1–P4

---

## Reference files

- `references/test-case-template.md` — Full markdown template for a single test case file
- `references/xray-csv-guide.md` — Xray and TestRail column formats, field rules, and escaping rules
- `references/priority-guide.md` — Priority assignment criteria and examples
