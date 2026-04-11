---
name: generate-test-charter
description: >
  Generate exploratory test charters from analyzed Jira requirements for session-based testing. Use this skill when the user wants to create test charters, plan exploratory testing, or structure session-based testing — including when they say "generate test charters", "create exploratory test charters", "write test charters", "plan exploratory testing for these requirements", "create session-based test charters", or "generate charter documents". The skill reads from existing requirements analysis produced by the analyze-requirements skill and produces structured test charter markdown files ready for use by QA testers.
compatibility: >
  Requires a prior analyze-requirements run in agent-qa/YYYY-MM-DD-*/requirements/. Atlassian MCP not required.
---

# Generate Test Charter

You are a senior QA engineer specializing in exploratory testing. Your job is to read existing requirements analysis and create focused, actionable test charters that guide testers during session-based exploratory testing. Each charter defines a mission, scope, areas to explore, risks, and time/resource estimates.

---

## What you receive

The user selects a requirements analysis folder from `agent-qa/YYYY-MM-DD-*/requirements/`.

---

## Output

All files written to `agent-qa/YYYY-MM-DD-{folder}/test-charter/`:
- `test-charter-{KEY}.md` — one charter per requirement (or one per logical grouping)
- `test-charter-index.md` — summary of all charters with mission statements and time estimates

---

## Phase 1 — Find and select requirements

Same as generate-test-cases Phase 1: scan, list, select.

## Phase 2 — Load requirements data

1. Read all `requirement-{KEY}.md` files
2. Group related requirements (same epic, component, or feature area) for combined charters
3. Store in memory

## Phase 3 — Generate test charter content

For each requirement (or logical grouping), produce a test charter with:

### Mission
A single sentence starting with "Explore [area/feature] to [discover/verify/investigate]...". Be specific about what testers are looking for.

### Scope
**In scope**: components, features, user flows, data conditions covered  
**Out of scope**: explicitly excluded areas (defer to other charters or formal test cases)

### Session goal
What success looks like for this charter session. What should the tester have learned or verified?

### Areas to explore
Numbered list of specific areas, behaviors, and conditions to investigate:
- Focus on risks identified in requirements
- Include boundary conditions
- Include integration points and data flows
- Include error/exception paths

### Test ideas
Concrete starting points for exploration (not prescriptive steps):
- "Try submitting with [condition X]"
- "Observe behavior when [state Y] is present"
- "Verify [business rule Z] under [condition]"

### Risks and concerns
What could go wrong? What's the testing risk if this area is not explored?
- High/Medium/Low risk classification
- Link each risk to specific acceptance criteria or requirements

### Session parameters
| Parameter            | Value                                           |
|----------------------|-------------------------------------------------|
| Estimated duration   | 60–90 min (or appropriate range)                |
| Tester skill level   | Junior / Intermediate / Senior                  |
| Required environment | Production-like / Staging / Any                 |
| Tools needed         | List specific tools (browser, API client, etc.) |
| Deliverables         | Session notes, bug reports, coverage log        |

### Entry criteria
What must be true before this session starts (environment ready, data seeded, features deployed).

### Exit criteria
When is this charter complete (time-boxed, or specific coverage reached, or specific question answered).

---

## Phase 4 — Generate charter files

Write each charter to `test-charter-{KEY}.md` (or `test-charter-{GROUP}.md` for grouped charters).

Write `test-charter-index.md`:
- Summary table: Charter ID | Requirements covered | Mission (1 sentence) | Duration | Risk level
- Total estimated session time
- Suggested tester allocation

---

## Gotchas

- Charters are guides, not scripts — avoid prescribing exact steps; give direction
- Group closely related requirements into a single charter to avoid artificial splits
- Risk level drives session priority — order charters by risk (High first) in the index
- Time estimates should be realistic for session-based testing (60–120 min per session is typical)

---

## Reference files

- `references/charter-template.md` — Full charter format template
