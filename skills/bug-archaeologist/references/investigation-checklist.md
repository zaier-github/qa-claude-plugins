# Investigation Checklist

Use this as a quick quality gate before writing the Bug Biography. Check off each item
that was attempted. Note "N/A" or "unavailable" where applicable — don't skip silently.

## Git History
- [ ] `git log --oneline -20 -- <file>` — file's recent history reviewed
- [ ] `git blame -L <range>` — line-level attribution obtained for bug site
- [ ] `git show <commit>` — introduction commit examined in full
- [ ] `git log -L :<function>:<file>` — function-level history traced (if supported)
- [ ] `git diff <good>..<bad>` — diff between working and broken states captured
- [ ] `git log --grep` — commit messages searched for relevant keywords
- [ ] `git log --follow` — file renames tracked (if file was moved/renamed)

## Context
- [ ] Original intent of the code understood (earliest commit examined)
- [ ] Timeline of significant changes assembled
- [ ] "Moment of introduction" identified to a specific commit
- [ ] PR or branch context identified (if available)

## Tests
- [ ] Test files covering this code path located
- [ ] Test history for those files reviewed
- [ ] Coverage gap (if any) documented
- [ ] Whether tests existed *before* the bug's introduction determined

## Structural Signals
- [ ] TODO/FIXME/HACK comments near bug site checked
- [ ] Contributing factors identified (see template section)
- [ ] Recommendations drafted

## Output Quality
- [ ] Executive Summary readable by a non-engineer
- [ ] All commit references include hash + author + date
- [ ] No unsubstantiated blame toward individuals
- [ ] Gaps in investigation honestly documented
- [ ] Evidence log populated with supporting raw data
- [ ] Both `bug-biography.md` and `evidence-log.md` saved