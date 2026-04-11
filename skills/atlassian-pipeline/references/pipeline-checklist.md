# Pipeline Execution Checklist

Use this checklist to verify each step completed successfully before proceeding to the next.

---

## Pre-flight checks

- [ ] Atlassian MCP server accessible (`mcp_Atlassian_getAccessibleAtlassianResources` responds)
- [ ] If `include_commits: true`: Git MCP server accessible for the configured platform
- [ ] Jira input is valid (issue key format or JQL syntax)
- [ ] Output base folder determined (`YYYY-MM-DD-{scope}/`)

---

## Step 1: analyze-requirements

**Verify complete**:
- [ ] `agent-qa/YYYY-MM-DD-{scope}/requirements/` folder exists
- [ ] `requirements-index.md` exists with summary statistics
- [ ] At least one `requirement-{KEY}.md` file exists
- [ ] No error messages about MCP connection failure

**Key info to note for downstream steps**:
- Base folder path: `_________________`
- Number of requirements: `_________________`
- Any requirements with missing AC: `_________________`

---

## Step 2: analyze-commits (conditional)

_Skip if `include_commits: false` (default)_

**Verify complete**:
- [ ] `agent-qa/YYYY-MM-DD-{scope}/commits/` folder exists
- [ ] `commits-index.md` exists
- [ ] At least one `{KEY}-commits.md` file exists (or explicitly states "no commits found")

---

## Step 3: generate-test-charter

**Verify complete**:
- [ ] `agent-qa/YYYY-MM-DD-{scope}/test-charter/` folder exists
- [ ] `test-charter-index.md` exists
- [ ] At least one `test-charter-*.md` file exists

---

## Step 4: generate-test-strategy

**Verify complete**:
- [ ] `agent-qa/YYYY-MM-DD-{scope}/test-strategy/` folder exists
- [ ] `test-strategy.md` exists

---

## Step 5: generate-test-cases

**Verify complete**:
- [ ] `agent-qa/YYYY-MM-DD-{scope}/test-cases/` folder exists
- [ ] `test-cases-index.md` exists
- [ ] At least one `test-cases-{KEY}.md` file exists
- [ ] `xray-bulk-import.csv` exists
- [ ] `test-cases-traceability-matrix.md` exists

---

## Step 6: generate-risk-register

**Verify complete**:
- [ ] `agent-qa/YYYY-MM-DD-{scope}/risk-register/` folder exists
- [ ] `risk-register.md` exists

---

## Step 7: generate-test-plan

**Verify complete**:
- [ ] `agent-qa/YYYY-MM-DD-{scope}/test-plan/` folder exists
- [ ] `test-plan.md` exists

---

## Pipeline complete

**Final folder structure**:
```
agent-qa/YYYY-MM-DD-{scope}/
├── requirements/
│   ├── requirements-index.md
│   └── requirement-{KEY}.md (× N)
├── commits/                      (if include_commits: true)
│   ├── commits-index.md
│   └── {KEY}-commits.md (× N)
├── test-charter/
│   ├── test-charter-index.md
│   └── test-charter-*.md (× N)
├── test-strategy/
│   └── test-strategy.md
├── test-cases/
│   ├── test-cases-index.md
│   ├── test-cases-{KEY}.md (× N)
│   ├── xray-bulk-import.csv
│   └── test-cases-traceability-matrix.md
├── risk-register/
│   └── risk-register.md
└── test-plan/
    └── test-plan.md
```
