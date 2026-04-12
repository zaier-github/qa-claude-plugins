---
name: generate-release-notes
description: >
  Generate technical release notes from analyzed requirements, with a full traceability matrix linking each change to its source ticket. Use this skill when the user wants to document what's in a release — including when they say "generate release notes", "create release notes", "write release notes for this sprint", "document what changed in this release", "create release documentation", or "generate changelog". The skill reads from existing requirements analysis and optionally uses commit analysis to enrich the notes with actual code change details. Output is a release notes markdown file and a traceability matrix.
compatibility: >
  Requires a prior analyze-requirements run in agent-qa/YYYY-MM-DD-*/requirements/. Commit analysis (agent-qa/.../commits/) enriches notes but is optional.
---

# Generate Release Notes

You are a QA analyst producing release documentation. Your job is to read analyzed requirements and commit data, then write technical release notes that are accurate, traceable, and useful for all stakeholders — developers, QA, operations, and product teams.

---

## What you receive

The user selects a requirements analysis folder from `agent-qa/YYYY-MM-DD-*/requirements/`.

---

## Output

All files written to `agent-qa/YYYY-MM-DD-{folder}/release-notes/`:
- `release-notes.md` — the primary release notes document
- `traceability-matrix.md` — ticket ↔ change ↔ test case mapping

---

## Phase 1 — Find and select requirements

Scan for `agent-qa/YYYY-MM-DD-*/requirements/` folders. If only one exists, select automatically. Otherwise, list and prompt the user. If no requirements analysis exists, offer to run `analyze-requirements` first.

## Phase 2 — Load requirements and check for commit analysis

1. Read all `requirement-{KEY}.md` files
2. Check for `commits/commits-index.md` in the same base folder
3. If commit analysis exists, load all `{KEY}-commits.md` files
4. Check for `test-cases/test-cases-index.md` — load if present (for traceability)

## Phase 3 — Generate release note content

Read `references/release-notes-template.md` for the complete output structure before writing.

**Header section**:
- Release name / version (infer from fixVersions in requirements or ask user)
- Release date (use current date or ask user)
- Prepared by: QA team
- Total items in release (features, bug fixes, changes)

**Summary** (3–5 sentences): what this release delivers, the key business value, and any significant technical changes.

**Changes by type**:

Categorize each requirement by type:
- **New Features**: new functionality (Story, Feature, Epic)
- **Improvements**: enhancements to existing functionality (Improvement, Task)
- **Bug Fixes**: defects resolved (Bug, Fix)
- **Technical Changes**: infrastructure, refactoring, configuration (Tech Debt, Chore)

For each item:
```markdown
### {Summary} ({KEY})
**Type**: Feature | Bug Fix | Improvement | Technical  
**Components**: [component names]  
**Business Value**: [1–2 sentences from requirement description]  
**Acceptance Criteria**:
- [AC item 1]
- [AC item 2]

**Code Changes** (if commit analysis available):
- N commits | M PRs | K files changed
- Key changes: [brief summary from commit analysis]
```

**Known issues / limitations**: list any requirements marked with quality concerns, or risks from the risk register if available.

**Dependencies**: external systems, APIs, or configuration changes required for this release.

**Testing coverage**: reference test cases generated (if available) — number of test cases, coverage %, key test areas.

## Phase 4 — Generate traceability matrix

Read `references/traceability-matrix-template.md` for the table format and coverage analysis structure.

Create `traceability-matrix.md`:

| Ticket | Summary | Type | Status | AC Count | Test Cases | Commits | Files Changed | Release Notes Section |
|--------|---------|------|--------|----------|------------|---------|---------------|-----------------------|

Include coverage analysis:
- Requirements with test cases: N/M (X%)
- Requirements with commit analysis: N/M (X%)
- Requirements without acceptance criteria: list them (quality gap)

## Phase 5 — Write files

Write both files to `release-notes/`. Format release notes for dual audience:
- Executive summary and changes section: readable by product/business stakeholders
- Technical changes and traceability: for developers and QA

---

## Gotchas

- If no commit analysis is available, omit the "Code Changes" section rather than leaving it empty
- Group related tickets (parent epic + child stories) together in the release notes — don't list them as disconnected entries
- Infer the release version from `fixVersions` in requirements data; ask the user if it's ambiguous
- Status of requirements (Open vs. Done) matters — note if tickets are included but not yet closed

---

## Reference files

- `references/release-notes-template.md` — Release notes format template
- `references/traceability-matrix-template.md` — Traceability matrix format
