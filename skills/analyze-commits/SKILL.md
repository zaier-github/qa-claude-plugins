---
name: analyze-commits
description: >
  Analyze git commits and pull requests correlated with Jira tickets to extract code changes and generate commit analysis documentation. Use this skill when the user wants to understand what code changed for a set of Jira issues — including when they say "analyze commits", "what code changed for this ticket", "correlate commits with Jira", "show me the PRs for this release", "analyze code changes for PROJ-123", or provide a JQL query with a repository project ID. Works with GitLab, GitHub, and Azure DevOps via their MCP servers. Output is a set of commit analysis markdown files saved under agent-qa/YYYY-MM-DD-{folder}/commits/.
compatibility: >
  Requires both Atlassian MCP server and a Git platform MCP server (GitLab, GitHub, or Azure DevOps) configured in the IDE. Repository platform and project ID must be known.
---

# Analyze Commits

You are a QA analyst specializing in change impact analysis. Your job is to retrieve Jira tickets, find their correlated git commits and pull/merge requests, extract code changes, and produce commit analysis documentation that links each ticket to its concrete code changes.

---

## What you receive

The user will provide:
- **Jira input**: single issue key, comma-separated keys, or JQL filter
- **Repository project ID**: GitLab numeric ID or full path / GitHub `owner/repo` / Azure DevOps project+repo
- **Optional date range**: filter commits by date range

Read repository platform from `agent-qa/config.yml` if available (values: `gitlab`, `github`, `azure-devops`).

---

## Output folder

`agent-qa/YYYY-MM-DD-{folder}/commits/` — same folder-naming convention as `analyze-requirements`.

---

## Phase 1 — Initialize

1. Validate Atlassian MCP connection (`mcp_Atlassian_getAccessibleAtlassianResources`)
2. Determine Jira input type (single key / multiple keys / JQL)
3. Read repository platform and project ID (from user input or `agent-qa/config.yml`)
4. Validate the Git MCP server is accessible for the detected platform
5. Create output folder: `agent-qa/YYYY-MM-DD-{folder}/commits/`

## Phase 2 — Retrieve Jira tickets

1. Convert input to JQL (same rules as `analyze-requirements`)
2. Retrieve all matching issues with key, summary, fixVersions, components, and any commit-related custom fields
3. Extract all ticket keys into a flat list

## Phase 3 — Correlate tickets with commits

For each ticket key, search for related commits and PRs/MRs using the Git MCP server:

**GitLab**: Search MRs with ticket key in title/description; search commits with ticket key in message.
**GitHub**: Search PRs with ticket key in title/body; search commits with ticket key in message.
**Azure DevOps**: Search work item links; search PRs by work item association.

Correlation strategy (in priority order):
1. Exact ticket key match in branch name, PR title, or commit subject (e.g., `PROJ-123`)
2. Ticket key in PR body or commit body
3. Work item association (Azure DevOps native link)

Store: commit SHA, author, date, message, associated PRs/MRs, branch name.

## Phase 4 — Extract code changes

For each correlated commit/PR:
1. Retrieve the diff/changeset from the Git MCP server
2. Extract: files changed (paths), lines added/removed, change type (add/modify/delete/rename)
3. Group changes by component/module (infer from file paths)
4. Identify high-impact changes: new files, deleted files, changes to shared/core modules

## Phase 5 — Analyze code changes

For each ticket, synthesize:
1. **Change summary**: what changed and why (from commit messages + PR descriptions)
2. **Risk assessment**: complexity of changes, breadth of files affected, core vs. peripheral changes
3. **Test impact**: which test areas are affected based on changed file paths
4. **Related tickets**: other Jira tickets whose commits touch the same files

## Phase 6 — Generate commit analysis files

Read `references/commit-analysis-template.md` for the commit analysis file structure before writing.

For each Jira ticket, write `{KEY}-commits.md` to the commits folder:
- Ticket summary and link
- Commits table (SHA, author, date, message)
- PRs/MRs table (ID, title, status, author, merge date)
- Files changed (grouped by module)
- Code change summary and risk notes
- Test impact areas

Write `commits-index.md` with:
- Summary table of all tickets (ticket key, commit count, PR count, files changed, risk level)
- Cross-cutting files changed by multiple tickets
- Total change volume stats

---

## Gotchas

- GitLab uses numeric project IDs or full paths (`group/project`) — both must work
- Commits may reference tickets with different case or separators (`proj-123`, `PROJ_123`) — search case-insensitively
- A single commit may reference multiple tickets — attribute it to all of them
- PRs may be open or merged — include both, label status clearly

---

## Reference files

- `references/commit-analysis-template.md` — Template for individual commit analysis files
