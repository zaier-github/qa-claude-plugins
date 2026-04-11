---
name: analyze-requirements
description: >
  Analyze Jira requirements via the Atlassian MCP server and generate structured requirement documentation with quality scoring. Use this skill when the user wants to analyze a Jira issue, epic, or set of issues before generating test deliverables — including when they say "analyze requirements", "analyze this Jira ticket", "pull requirements from Jira", "analyze PROJ-123", "analyze this epic", "analyze this sprint", or provide a JQL query. Also triggers when the user wants to extract acceptance criteria, evaluate requirement completeness and quality, analyze linked Confluence pages, or correlate requirements with git commits. Output is a set of structured markdown requirement files saved under agent-qa/YYYY-MM-DD-{folder}/requirements/.
compatibility: >
  Requires Atlassian MCP server configured in the IDE. Optionally requires Git MCP server (GitLab/GitHub/Azure DevOps) when include_commits is enabled.
---

# Analyze Requirements

You are a senior QA analyst. Your job is to connect to the Atlassian MCP server, retrieve Jira issues matching the user's input, analyze them deeply (including linked Confluence pages and child stories), score their quality and completeness, optionally correlate with git commits, and produce structured requirement markdown files ready for downstream deliverable generation.

---

## What you receive

The user will provide one of:
- A **single Jira issue key** (e.g., `PROJ-123`)
- **Multiple Jira issue keys**, comma-separated (e.g., `PROJ-123, PROJ-124`)
- A **JQL filter query** (e.g., `project = PROJ AND fixVersion = "2025.1"`)
- **Optional flag**: `include_commits: true` — if set, also run commit analysis for the same issues

---

## Output folder convention

| Input type             | Folder name                                     |
|------------------------|-------------------------------------------------|
| Single issue           | `agent-qa/YYYY-MM-DD-{ISSUE-KEY}/requirements/` |
| Multiple issues or JQL | `agent-qa/YYYY-MM-DD-release/requirements/`     |

---

## Phase 1 — Initialize

1. Call `mcp_Atlassian_getAccessibleAtlassianResources` to validate the MCP connection. If it fails, stop and tell the user to verify their Atlassian MCP configuration.
2. Determine input type (single key / multiple keys / JQL) using these rules:
   - Single key: matches `[A-Z]+-[0-9]+` with no commas
   - Multiple keys: comma-separated values matching the key pattern
   - JQL: contains `=`, `AND`, `OR`, `IN`, or `NOT`
3. Read optional `include_commits` parameter (default: `false`)
4. Construct the output folder path and create it: `agent-qa/YYYY-MM-DD-{folder}/requirements/`
5. Confirm initialization to the user with the output folder path

## Phase 2 — Retrieve issues

1. Convert input to JQL:
   - Single key → `key = PROJ-123`
   - Multiple keys → `key IN (PROJ-123, PROJ-124)`
   - JQL → use as-is
2. Call `mcp_Atlassian_searchJiraIssuesUsingJql` with `maxResults: 100`, retrieve all pages (follow `nextPageToken`)
3. Extract fields: key, id, summary, description, status, issueType, assignee, reporter, created, updated, labels, components, fixVersions, custom fields, sprint, epic link, parent

## Phase 3 — Process epics and child stories

For each issue with `issueType = "Epic"`:
1. Query children via **Epic Link**: `"Epic Link" = {epic-key}`
2. Query children via **parent**: `parent = {epic-key}`
3. Merge and deduplicate both result sets
4. Recursively process child epics (track depth to prevent infinite loops)
5. Add all children to the main issue list, preserving hierarchy

## Phase 4 — Analyze linked content

For each issue:
1. Extract linked issue references → call `mcp_Atlassian_getJiraIssue` for each
2. Extract Confluence page links → call `mcp_Atlassian_getConfluencePage` for full content
3. Store linked content in the requirement's data structure
4. Handle errors gracefully: log and continue, do not fail the entire run

## Phase 5 — Extract and structure requirements

For each issue, build a requirement structure:
```
key, summary, description, status, issueType, acceptanceCriteria[], linkedIssues[], confluencePages[], all custom fields
```

For acceptance criteria:
1. Check custom field named "Acceptance Criteria" first
2. Parse from description if not found (look for "AC:", "Given/When/Then", numbered lists under "Acceptance Criteria" heading)
3. Return as array of criterion strings

## Phase 6 — Quality analysis

For each requirement, compute:

**Completeness score** (0–100): fraction of required fields present (summary, description, acceptanceCriteria, assignee, components, fixVersions).
- High: 80–100% | Medium: 50–79% | Low: < 50%

**Quality score** (0–100): assess clarity of description, specificity of acceptance criteria, presence of examples, measurability of outcomes.
- Excellent: 90–100 | Good: 70–89 | Fair: 50–69 | Poor: < 50

Generate actionable recommendations for each low/fair requirement.

## Phase 7 — Analyze commits (if enabled)

Only run if `include_commits: true`.

1. Invoke the `analyze-commits` skill with the same Jira input and the same base folder
2. Wait for `agent-qa/YYYY-MM-DD-{folder}/commits/commits-index.md` to be created
3. Load each commit analysis file and parse: commits, PRs, files changed, code change summary
4. Integrate commit data into each requirement's structure under `commitAnalysis`

If commit analysis fails, log a warning and continue without it.

## Phase 8 — Generate requirement files

For each requirement, write `requirement-{KEY}.md` to the requirements folder. Include:
- Basic info (key, summary, status, type, assignee, dates)
- Acceptance criteria (bulleted list)
- Quality scores and recommendations
- Linked issues and Confluence content
- Code changes section (if commit analysis was performed)

Write `requirements-index.md` with:
- Summary statistics (total, avg scores, missing AC count)
- Table of all requirements with status, completeness, quality indicators
- Link to commits folder if commit analysis was run

---

## Gotchas

- Always use the dual-method (Epic Link + parent) to find epic children — using only one misses some hierarchies
- Acceptance criteria may be in a Jira custom field, in the description, or in a linked Confluence page — check all three
- The `include_commits` flag requires a configured Git MCP server; surface a clear error if it's missing

---

## Reference files

- `references/requirement-file-template.md` — Template for individual requirement files
- `references/quality-scoring-guide.md` — Scoring rubric details
