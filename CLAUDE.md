# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A **Claude Code plugin** (`qa-engineering`) that ships 21 QA-focused skills in two groups: standalone analysis skills (no external services required) and Jira-integrated pipeline skills (require the Atlassian MCP server). There is no build step, no test runner, and no compiled output — every artifact is a markdown file. Changes take effect after reloading the plugin in Claude Code.

## Plugin identity

- **Plugin name**: `qa-engineering` (declared in `.claude-plugin/plugin.json`)
- **Marketplace manifest**: `.claude-plugin/marketplace.json`
- **Plugin root**: the repository root (skills resolved from `skills/`)
- **Version**: bump `version` in `.claude-plugin/plugin.json` when cutting a consumer-visible release

## Skill structure

Each skill lives under `skills/<skill-name>/` and follows this layout:

| File/dir          | Purpose                                                          |
|-------------------|------------------------------------------------------------------|
| `SKILL.md`        | Frontmatter (`name`, `description`) + full workflow instructions |
| `references/*.md` | Templates, rubrics, and guides the skill reads while working     |
| `agents/*.md`     | Subagent briefs for parallel work on large inputs (optional)     |

**The `description` field in `SKILL.md` frontmatter is the primary routing signal** — Claude matches user intent against it to decide which skill to invoke. Keep it long, trigger-word-rich, and accurate.

## Skills in this repo

### Standalone analysis skills (no MCP required)

| Skill                    | Output artifact                                                  |
|--------------------------|------------------------------------------------------------------|
| `the-skeptic`            | Assumption Log — surfaces gaps in a spec before coding starts    |
| `regression-oracle`      | Pre-Flight Checklist — predicts what could break from a diff/PR  |
| `mutation-jury`          | Verdict Report — triages surviving mutants from mutation testing |
| `test-debt-cartographer` | Coverage Risk Map — prioritizes undertested hot spots            |
| `bug-archaeologist`      | Bug Biography — reconstructs the origin story of a defect        |
| `chaos-playwright`       | Adversarial UI test scenarios via dysfunctional user archetypes  |
| `contract-whisperer`     | Breaking Change Impact Story — detects API/schema drift          |

### Jira-integrated pipeline skills (require Atlassian MCP)

These skills form a sequential pipeline. Most downstream skills depend on a prior `analyze-requirements` run; outputs land in `agent-qa/YYYY-MM-DD-{folder}/`.

| Skill                    | Phase        | Notes                                                                       |
|--------------------------|--------------|-----------------------------------------------------------------------------|
| `analyze-requirements`   | Planning     | Entry point — fetches Jira issues, scores requirement quality               |
| `analyze-commits`        | Planning     | Requires Atlassian MCP + Git platform MCP (GitLab/GitHub/Azure DevOps)      |
| `generate-test-charter`  | Planning     | Requires prior `analyze-requirements` output                                |
| `generate-test-strategy` | Planning     | Requires prior `analyze-requirements` output                                |
| `generate-test-cases`    | Planning     | Requires prior `analyze-requirements`; exports Xray or TestRail CSV          |
| `generate-risk-register` | Planning     | Requires prior `analyze-requirements`; best with charter + strategy + cases |
| `generate-test-plan`     | Planning     | Requires prior `analyze-requirements`; best with all other artifacts        |
| `generate-release-notes` | Planning     | Requires prior `analyze-requirements`; enriched by commit analysis          |
| `quality-auditor`        | Execution    | Defect density, coverage, pass rate, bottleneck dashboard                   |
| `maturity-coach`         | Execution    | Automation maturity score (0–5) and coaching roadmap                        |
| `process-optimizer`      | Execution    | Bottleneck detection + improvement Jira ticket creation                     |
| `release-gatekeeper`     | Reporting    | Weighted GO/NO-GO recommendation                                            |
| `roi-analyst`            | Reporting    | Financial ROI for test automation investment                                |
| `atlassian-pipeline`     | Orchestrator | Runs the full pipeline end-to-end in one command                            |

## Multi-agent pattern

Skills document their own thresholds for when to fan out. The general contract:
1. The **skill** (`SKILL.md`) acts as orchestrator — it decides if the input is large enough to warrant subagents.
2. **Subagents** (`agents/*.md`) each receive a narrow mandate and write findings to a `findings/` directory.
3. The skill merges, deduplicates, normalizes severity/IDs, and writes the single user-facing artifact.

Do not spawn subagents for small inputs — coordination overhead outweighs the benefit.

## Making changes

- **Adjust behavior**: edit `SKILL.md` workflow steps or its `description` frontmatter.
- **Adjust output format**: edit the corresponding template under `references/`.
- **Adjust subagent focus**: edit the relevant `agents/*.md` brief.
- **Validate**: after editing, reload the plugin in Claude Code and test with a minimal fixture (a short diff, small mutation report, or one-page spec).

## Key conventions

- `SKILL.md` frontmatter must be valid YAML with at minimum `name` and `description`.
- Reference file paths in skill workflows are relative to the skill directory (e.g. `references/risk-classification.md` resolves to `skills/regression-oracle/references/risk-classification.md`).
- Jira-integrated skill outputs go to `agent-qa/YYYY-MM-DD-{folder}/` in the **user's current working directory**. Standalone skill outputs are also written to the user's CWD unless specified otherwise.
- Inline conversation summaries are always produced alongside the saved artifact so the user gets immediate signal without opening the file.
- The `atlassian-pipeline` skill orchestrates pipeline skills in order: `analyze-requirements` → `analyze-commits` (optional) → `generate-test-charter` → `generate-test-strategy` → `generate-test-cases` → `generate-risk-register` → `generate-test-plan`.
