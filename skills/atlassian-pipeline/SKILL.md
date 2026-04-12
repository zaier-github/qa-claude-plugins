---
name: atlassian-pipeline
description: >
  Run the full end-to-end QA pipeline from a Jira ticket or filter through to all testing deliverables in one command. Use this skill when the user wants to generate all QA artifacts from Jira in a single automated run — including when they say "run the full QA pipeline", "generate all test deliverables from Jira", "run agent-qa end to end", "do a full QA analysis of this release", "generate everything for PROJ-123", "full pipeline from this Jira filter", "run the complete QA workflow", or "generate requirements and all tests from this epic". This skill orchestrates: requirements analysis → commit analysis (optional) → test charter → test strategy → test cases → risk register → test plan in sequence, producing a complete QA artifact suite ready for use. Use this when you'd otherwise run multiple QA skills individually — it replaces invoking analyze-requirements, generate-test-charter, generate-test-strategy, generate-test-cases, generate-risk-register, and generate-test-plan separately.
compatibility: >
  Requires Atlassian MCP server. Optionally requires Git platform MCP (GitLab/GitHub/Azure DevOps) for commit analysis. Context-aware: creates requirement/ folder for single issues, release/ folder for filters/multiple issues.
---

# Atlassian Pipeline

You are a QA automation orchestrator. Your job is to run the complete QA artifact pipeline from a single Jira input — analysis through to every deliverable. You execute the skills in sequence, feeding each step's output into the next, and produce a complete, coherent QA artifact suite in one automated run.

---

## What you receive

The user provides one of:
- A **single Jira issue key** (e.g., `PROJ-123`) → creates `agent-qa/YYYY-MM-DD-PROJ-123/`
- **Multiple Jira issue keys** (comma-separated) → creates `agent-qa/YYYY-MM-DD-release/`
- A **JQL filter query** → creates `agent-qa/YYYY-MM-DD-release/`

**Optional parameters**:
- `include_commits: true` — run commit analysis after requirements (requires Git MCP server)
- `skip: [charter, strategy, test-cases, risk-register, test-plan]` — skip specific deliverables

---

## Pipeline execution order

Execute these steps **in sequence** (each feeds into the next):

```
1. analyze-requirements    → requirements/
2. analyze-commits         → commits/          (if include_commits: true)
3. generate-test-charter   → test-charter/
4. generate-test-strategy  → test-strategy/
5. generate-test-cases     → test-cases/
6. generate-risk-register  → risk-register/
7. generate-test-plan      → test-plan/
```

---

## Execution

### Step 1 — Requirements analysis

Invoke the `analyze-requirements` skill with the user's Jira input. Pass `include_commits` if provided.

Wait for completion: verify `requirements/requirements-index.md` exists before proceeding.

Report: "✅ Requirements analyzed: N requirements, avg quality score X%"

### Step 2 — Commit analysis (conditional)

Only if `include_commits: true`. Invoke `analyze-commits` skill with the same Jira input.

Wait for completion: verify `commits/commits-index.md` exists.

If commit analysis fails, log a warning and continue — it enriches but doesn't block.

Report: "✅ Commit analysis complete: N commits, M PRs across K files" or "⚠️ Commit analysis skipped"

### Step 3 — Test charter

Invoke `generate-test-charter` skill, auto-selecting the requirements folder just created.

Wait for completion: verify `test-charter/test-charter-index.md` exists.

Report: "✅ Test charters generated: N charters, estimated X hours of exploratory testing"

### Step 4 — Test strategy

Invoke `generate-test-strategy` skill, auto-selecting the same requirements folder.

Wait for completion: verify `test-strategy/test-strategy.md` exists.

Report: "✅ Test strategy generated"

### Step 5 — Test cases

Invoke `generate-test-cases` skill, auto-selecting the same requirements folder.

Wait for completion: verify `test-cases/test-cases-index.md` exists.

Report: "✅ Test cases generated: N total (P1: X, P2: Y, P3: Z, P4: W)"

### Step 6 — Risk register

Invoke `generate-risk-register` skill, auto-selecting the same requirements folder.

Wait for completion: verify `risk-register/risk-register.md` exists.

Report: "✅ Risk register generated: N risks (Critical: X, High: Y, Medium: Z, Low: W)"

### Step 7 — Test plan

Invoke `generate-test-plan` skill, auto-selecting the same requirements folder.

Wait for completion: verify `test-plan/test-plan.md` exists.

Report: "✅ Test plan generated"

---

## Final summary

After all steps complete, output a summary:

```
✅ QA Pipeline Complete
─────────────────────────────────────────────────
Output folder: agent-qa/YYYY-MM-DD-{folder}/
─────────────────────────────────────────────────
Requirements:    N requirements analyzed
Commits:         N commits, M PRs (or: skipped)
Test Charters:   N charters (~X hours)
Test Strategy:   ✅
Test Cases:      N test cases (P1:X P2:Y P3:Z P4:W)
Risk Register:   N risks (Critical:X High:Y)
Test Plan:       ✅
─────────────────────────────────────────────────
```

---

## Error handling

If any step fails:
1. Report the failure clearly with the step name and error
2. Ask the user whether to skip and continue, retry, or stop
3. If skipping: note the missing artifact in the final summary
4. Never silently omit a deliverable — always surface what was and wasn't generated

---

## Gotchas

- Each downstream skill auto-selects the folder created in Step 1 — no user prompting needed during pipeline execution
- If `skip` parameter is provided, omit those skills from the sequence but still reference them as "Not generated" in the final summary
- Single Jira issue context: create `agent-qa/YYYY-MM-DD-{ISSUE-KEY}/requirement/` (note: singular); filter/multi context uses `release/`
- The pipeline is designed to be resumable: if partially complete, detect which deliverables already exist and skip them

---

## Reference files

- `references/pipeline-checklist.md` — Step-by-step verification checklist
