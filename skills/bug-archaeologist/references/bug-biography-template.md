# Bug Biography: [Short Descriptive Title]

> **File:** `path/to/affected/file.py` | **Function/Class:** `function_or_class_name`
> **Introduced:** `YYYY-MM-DD` | **Commit:** `abc1234` | **Author:** Name
> **Severity:** [Critical / High / Medium / Low] | **Type:** [Logic Error / Regression / Missing Guard / Race Condition / etc.]

---

## Executive Summary

_2–4 sentences. Describe what the bug does, when it was introduced, and why it happened — in terms a non-engineer can follow. No jargon. This is what goes in the incident ticket._

**Example:**
> A discount calculation introduced in the v2.3 pricing refactor silently returns negative totals
> when more than 3 coupons are stacked. The error was introduced on March 4th when the stacking
> logic was rewritten to support a new loyalty tier, but the boundary check from the original
> implementation was not carried over. No automated test covered this scenario at the time.

---

## The Story

### Origin: What the code was trying to do

_Explain the original intent of the affected code. When was it first written, and what problem was it solving? Use `git log --follow` and early commit messages to reconstruct this context.
Be specific: name the commit and author, but don't cast blame._

---

### Evolution: How the code changed over time

_Walk through the significant changes to this code section, in chronological order. Each milestone should answer: what changed, who changed it, and why (as best you can infer from commit messages, PR descriptions, or code comments)._

**Timeline of changes:**

| Date       | Commit    | Author | What Changed      | Why (inferred)                     |
|------------|-----------|--------|-------------------|------------------------------------|
| YYYY-MM-DD | `abc1234` | Name   | Brief description | Refactor / Feature / Fix / Unknown |
| YYYY-MM-DD | `def5678` | Name   | Brief description | ...                                |

---

### The Moment of Introduction

_This is the heart of the Biography. Describe the specific commit (or sequence of commits) where the bug was introduced. Be precise:_

- **Commit:** `hash` — [commit message]
- **Author:** Name, **Date:** YYYY-MM-DD
- **Part of:** [feature branch / hotfix / refactor / dependency upgrade / etc.]
- **What was changed:** [Describe the code change specifically]
- **What was lost:** [What existing behavior, guard, or logic was removed or altered]
- **Was it knowable?** [Could a reviewer have caught it? Was there a test that should have covered it?]

_Include a small diff snippet if it clearly illustrates the introduction point._

```diff
- original line(s) that prevented the bug
+ new line(s) that introduced it
```

---

### Why It Wasn't Caught

_Explain the gaps that allowed this bug to reach production (or wherever it was found).
Be specific and constructive — this is the section that drives real improvements._

- **Test coverage:** Were there tests for this path? When were they last updated?
- **Review context:** Was this a large PR? An emergency fix? A low-scrutiny commit?
- **Assumptions:** Did the code author make a reasonable assumption that turned out to be wrong?
- **Documentation:** Was expected behavior documented anywhere?

---

## Contributing Factors

_List the systemic or structural factors (beyond the immediate code change) that contributed to this bug existing. These are the inputs to your "lessons learned" section._

- [ ] No test coverage for this edge case
- [ ] Large refactor without updated tests
- [ ] Implicit behavior dependency not documented
- [ ] Missing input validation / guard clause
- [ ] Dependency version change with silent behavioral diff
- [ ] Other: _____

---

## Related Artifacts

_Links and references to supporting evidence._

| Type      | Reference               | Notes                            |
|-----------|-------------------------|----------------------------------|
| Commit    | `abc1234`               | Moment of introduction           |
| Commit    | `def5678`               | Prior working version            |
| PR/Issue  | #123                    | PR where change was merged       |
| Test File | `tests/test_pricing.py` | Coverage at time of introduction |
| Error Log | _if available_          | Stack trace or log snippet       |

See `evidence-log.md` for full supporting data (git blame excerpts, diffs, log output).

---

## Recommendations

_What should be done now and in the future to prevent recurrence? Be specific and actionable._

### Immediate
- [ ] [Fix or workaround for the current bug]
- [ ] [Add a regression test for this exact scenario]

### Process / Structural
- [ ] [Suggestion to improve test coverage in this module]
- [ ] [Suggestion for code review practice, documentation, or tooling]
- [ ] [Any refactoring that would make this class of bug harder to introduce]

---

## Investigation Notes

_Anything the investigator wants to flag: gaps in the git history, unclear commit messages,
areas that couldn't be fully traced, or follow-up questions for the original author._

---

*Biography generated by Bug Archaeologist skill | Investigated: YYYY-MM-DD*