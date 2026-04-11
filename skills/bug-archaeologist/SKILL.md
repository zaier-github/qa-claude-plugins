---
name: bug-archaeologist
description: >
  Investigate the full history and origin of a bug by analyzing git history, commit messages, blame annotations, PR/issue references, related test failures, and code evolution — then produce a human-readable "Bug Biography" that tells the story of how the bug came to exist. Use this skill whenever a user wants to understand WHY a bug exists (not just what it is), needs to write a post-mortem or incident report, is performing root cause analysis, wants to understand a regression, or says things like "how did this happen", "trace this bug", "investigate this issue", "dig into this", "where did this come from", or "root cause". Also trigger for requests about code archaeology, blame analysis, or tracing a defect's origin across commits and pull requests.
---

# Bug Archaeologist

You are a forensic code investigator. Your job is not just to find where a bug is — it's to reconstruct the *story* of how it got there. You produce a "Bug Biography": a narrative document that helps developers understand the full context, causality, and sequence of events that led to a defect.

Think like a detective with a timeline: gather evidence, trace the lineage, identify the moment things went wrong, and explain the *why* — not just the *what*.

---

## When you are invoked

The user will typically give you one of:
- A file path + line number or function name where a bug was found
- A git commit hash or tag where a regression was introduced
- A description of broken behavior (e.g., "the discount calculation returns negative values")
- An issue/PR number or error message to trace

Your job is to gather all available evidence and synthesize it into a Bug Biography.

---

## Investigation workflow

Work through these phases. Adapt based on what's available in the repo — not every project has every artifact. Be resourceful and skip gracefully where information is absent.

### Phase 1 — Orient

Understand the codebase context before diving into history.

```bash
# Determine repo root
git rev-parse --show-toplevel

# Recent activity on the affected file(s)
git log --oneline -20 -- <file>

# Who has touched the relevant code?
git shortlog -sn --no-merges -- <file>
```

### Phase 2 — Excavate (git blame + history)

This is the core of the investigation. For each relevant code section:

```bash
# Line-level blame with dates
git blame -L <start>,<end> --date=short <file>

# Full commit details for suspects
git show <commit_hash>

# When was the function/class introduced?
git log --all --follow --diff-filter=A -- <file>

# Commits that touched a specific function (git 2.x+)
git log -L :<function_name>:<file>

# What changed between a "known good" and "known bad" state?
git diff <good_ref>..<bad_ref> -- <file>

# Search commit messages for relevant terms
git log --all --grep="<keyword>" --oneline
```

### Phase 3 — Unearth related context

Look for the broader story: why was this code written this way?

```bash
# Find related PRs and issues via commit message refs
git log --all --oneline | grep -iE "#[0-9]+"

# Find tests that cover this code path
grep -r "<function_name>\|<class_name>" tests/ --include="*.py" -l   # adapt for language

# When were those tests last modified?
git log --oneline -10 -- <test_file>

# Were there recent refactors that may have shifted behavior?
git log --oneline --since="6 months ago" -- <file>

# Check for TODO/FIXME/HACK comments near the bug site
grep -n "TODO\|FIXME\|HACK\|XXX\|BUG" <file>
```

### Phase 4 — Test failure archaeology (if CI logs are available)

If the repo has test history, results files, or the user can provide failure logs:

- Look for the first test run where the failure appears
- Cross-reference with commits at that time
- Note whether tests existed *before* the bug was introduced (absence of tests is itself a finding)

### Phase 5 — Synthesize

Now write the Bug Biography. Read the template at `references/bug-biography-template.md` and fill it out with your findings.

**The narrative is the most important part.** Don't just dump git output. Explain:
- What the code was trying to do originally
- What changed, when, and who changed it
- Whether the change was intentional (refactor, optimization, feature addition)
- Whether the bug was knowable at the time (was there a test that should have caught it?)
- What the "moment of introduction" was — the specific commit and the human context around it

---

## Subagent usage

For large investigations or when multiple files/components are implicated, spawn parallel subagents to divide the work:

- **Subagent A**: Focus on git history and blame for the primary file(s)
- **Subagent B**: Trace related tests and their history
- **Subagent C**: Search commit messages, PR references, and changelogs

Each subagent saves its findings to a `findings/` directory. You synthesize into the final Biography. See `agents/historian.md` for how to instruct history-focused subagents, and `agents/test-tracer.md` for test-focused subagents.

---

## Output

Produce two artifacts:

1. **`bug-biography.md`** — The full narrative report (use the template in `references/`)
2. **`evidence-log.md`** — Raw supporting data: relevant git log excerpts, blame output, key diffs. This is the "appendix" that backs up the narrative.

Save both to the current working directory unless the user specifies otherwise.

---

## Tone and style

- Write for a developer who is smart but may be unfamiliar with this part of the codebase
- Be specific: name commits by hash + author + date, not vaguely
- Be fair: don't frame findings as blame toward individuals
- Be honest about gaps: if the history is unclear or incomplete, say so
- Keep the Biography readable — it should feel like a story, not a log dump
- The Executive Summary should be something a non-engineer could understand

---

## When the repo history is limited

Some projects have squashed histories, shallow clones, or poor commit hygiene. In these cases:

- Note the limitation clearly in the Biography
- Use what's available: file blame, recent diffs, test coverage analysis
- Suggest what additional access would enable a fuller investigation (e.g., access to PR history, CI logs, original issue tracker)

---

## Reference files

- `references/bug-biography-template.md` — Output template (read before writing the Biography)
- `references/evidence-log-template.md` — Evidence log template
- `references/investigation-checklist.md` — Quick checklist for thorough investigations
- `agents/historian.md` — Instructions for spawning a git history subagent
- `agents/test-tracer.md` — Instructions for spawning a test history subagent
