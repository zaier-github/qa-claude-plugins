# QA Claude Plugins

**Claude Code** plugin bundle for **AI-assisted QA workflows**: structured skills for requirements review, change-risk analysis, mutation triage, strategic coverage mapping, and bug forensics. Each skill is a self-contained package of instructions, reference docs, and optional **agent prompts** for parallel work on large inputs.

Plugin identity: **`qa-engineering`** (see [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json)).

---

## Repository Layout

```
qa-claude-plugins/
├── .claude-plugin/
│   ├── marketplace.json    # Marketplace manifest listing this plugin
│   └── plugin.json         # Plugin name, version, description, metadata
├── skills/                 # All installable skills (one directory per skill)
│   ├── bug-archaeologist/
│   ├── mutation-jury/
│   ├── regression-oracle/
│   ├── test-debt-cartographer/
│   └── the-skeptic/
└── README.md
```

Each skill directory follows a common shape:

| Path | Role |
|------|------|
| `SKILL.md` | Main skill definition: YAML frontmatter (`name`, `description`), workflow, outputs, when to delegate to agents |
| `references/` | Templates, rubrics, and deep guides the skill loads while working |
| `agents/` | Prompts for **focused subagents** (optional); used when work should be split in parallel |
| `scripts/` | Optional helper notes (e.g. [test-debt-cartographer/scripts/README.md](skills/test-debt-cartographer/scripts/README.md)) |

This repo does **not** ship a top-level `.claude/commands/` tree; it is **skill-first**. You can still combine these skills with your own project or global commands in Claude Code.

---

## Installing as a Plugin

You will use the files under [`.claude-plugin/`](.claude-plugin/):

1. **Clone or copy** this repository to a stable path on your machine (or publish it to a Git remote you control).
2. **Register the marketplace** in Claude Code using the path (or URL) to this repo’s **marketplace manifest**:  
   [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json)  
   The manifest lists one plugin, `qa-engineering`, with `"source": "./"`, meaning the **repository root** is the plugin root and `skills/` is resolved from there.
3. **Install the `qa-engineering` plugin** from that marketplace entry (exact menu or CLI wording depends on your Claude Code version).
4. **Confirm skills are visible** by starting a session in a project where the plugin is enabled and asking for a workflow that should match a skill (e.g. “review this PR for regression risk” → regression oracle).

**Remote installs:** Point the marketplace entry at your hosted `marketplace.json` (or the repo URL your Claude Code version accepts for plugins). **Local installs:** Use the absolute path to this checkout.

**Upstream reference:** `plugin.json` may declare a canonical URL (currently [github.com/zaier-github/qa-engineering](https://github.com/zaier-github/qa-engineering)); align that field with wherever you actually host the source of truth.

---

## Making and Testing Changes Locally

1. **Edit the skill you care about** under `skills/<skill-name>/`:
   - Adjust behavior in `SKILL.md` (frontmatter `description` strongly affects when Claude picks up the skill).
   - Update `references/` for templates and rubrics.
   - Update `agents/*.md` when you change how subagents should behave.
2. **Validate frontmatter** on `SKILL.md`: keep valid YAML and a clear `name` + `description` so the client can route tasks to the skill.
3. **Reload the plugin** in Claude Code after changes (restart session or refresh plugins, per your client).
4. **Dry-run in a disposable repo**: open a small sample project, enable this plugin, and invoke the skill with a minimal fixture (short diff, tiny mutation snippet, or a one-page spec) to confirm structure and tone of outputs.
5. **Regression-test “large input” paths**: for skills that document subagent thresholds (e.g. “100+ surviving mutants”, “large PRs”), use a trimmed but representative sample to ensure `agents/` instructions still read well and synthesis steps are clear.

Avoid committing machine-specific paths or secrets under `.claude/`; keep personal settings out of the shared plugin tree where possible.

---

## Skills vs Commands vs Agents

| Concept | What it is | In *this* repo |
|--------|------------|----------------|
| **Skills** | Packaged expertise: `SKILL.md` with metadata and procedures, plus optional references. Claude matches user intent to skill descriptions and follows the workflow. | **Primary content.** Five skills under `skills/`. |
| **Commands** | User-invoked shortcuts (often slash commands or CLI/project hooks) that run a fixed prompt or script. Typically live under `.claude/commands/` in a project or user config. | **Not included.** This bundle assumes natural-language invocation or your own commands that call into these skills. |
| **Agents** | Specialized **worker** instructions—usually a markdown file meant for a subagent or delegated model pass—with a narrow mandate (e.g. “only trace call sites”). | **Included** as `skills/*/agents/*.md`. The parent **skill** in `SKILL.md` decides *if* and *how* to use them; agents are not standalone plugins. |

**Mental model:** the **skill** is the playbook; **commands** (if you add them) are shortcuts to start a playbook; **agents** are optional chapter assignments when one playbook is too big for a single pass.

---

## Multi-Agent Workflows

Several skills describe **when to split work across parallel subagents**, where each subagent follows an `agents/*.md` brief and writes artifacts (often under a `findings/` directory) for the **lead** model to merge into one deliverable.

| Skill | When to parallelize | Typical agent split | Final artifact |
|-------|---------------------|---------------------|----------------|
| [regression-oracle](skills/regression-oracle/SKILL.md) | Large PRs, many files or subsystems | Call-site tracing vs data-contract auditing | Pre-Flight Checklist |
| [bug-archaeologist](skills/bug-archaeologist/SKILL.md) | Broad investigations, many implicated files | Git/history (`historian`) vs test history (`test-tracer`) | Bug Biography + evidence log |
| [the-skeptic](skills/the-skeptic/SKILL.md) | Large specs spanning domain + systems | Domain lens vs systems/integration lens | Assumption Log |
| [mutation-jury](skills/mutation-jury/SKILL.md) | Very large survivor lists (e.g. 100+) | Classifier batches vs test prescriptions | Verdict Report |
| [test-debt-cartographer](skills/test-debt-cartographer/SKILL.md) | Large multi-module repos | Coverage scoring vs structural patterns | Coverage Risk Map |

**Recommended pattern:** only fan out when the skill’s own thresholds say so—small inputs are intentionally handled **inline** to avoid coordination overhead. The orchestrating pass should **deduplicate**, **reconcile conflicts**, and **normalize IDs and severity** before shipping the single user-facing document.

---

## Skills at a glance

| Skill | One-line purpose |
|-------|------------------|
| [the-skeptic](skills/the-skeptic/SKILL.md) | Surface spec gaps and assumptions (**Assumption Log**). |
| [regression-oracle](skills/regression-oracle/SKILL.md) | Reason about diff/PR risk (**Pre-Flight Checklist**). |
| [mutation-jury](skills/mutation-jury/SKILL.md) | Triage surviving mutants (**Verdict Report**). |
| [test-debt-cartographer](skills/test-debt-cartographer/SKILL.md) | Prioritize undertested hot spots (**Coverage Risk Map**). |
| [bug-archaeologist](skills/bug-archaeologist/SKILL.md) | Tell the story of a defect (**Bug Biography**). |

---

## Contributing

Improve workflows, references, or agent prompts in `skills/` and bump **`version`** in [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json) when you cut a release consumers should notice.
