# Risk Classification

A framework for assigning severity tiers to identified regression risks. Use this to
ensure consistent, defensible prioritization in Pre-Flight Checklists.

---

## Tier Definitions

### 🔴 Critical

The change could cause data loss, security failure, financial error, or silent incorrect
behavior in a core system path — with no obvious way for users or monitors to detect it.

**Characteristics:**
- Silent data corruption (wrong values written, wrong records updated)
- Security boundary violated (auth check removed, permission logic altered, PII exposed)
- Financial calculation changed (price, tax, discount, fee, refund logic)
- Irreversible action now happens without the guard that was protecting it
- Database constraint removed that was preventing invalid states
- External API contract broken in a way consumers can't handle gracefully

**What to do:** Block or hold the PR. Require explicit sign-off from a domain owner.
Write a regression test before merging.

---

### 🟠 High

The change alters behavior in a significant, user-visible way on a commonly-traveled path,
or breaks a contract that multiple consumers depend on — but doesn't rise to data corruption
or security risk.

**Characteristics:**
- Behavioral change on a high-traffic code path (login, checkout, core API endpoint)
- API response shape change where consumers exist (even if those consumers may handle it)
- Shared utility modified in a way that affects many callers
- Exception handling changed in a way that silences errors that were previously surfaced
- Async/sync boundary changed in a way that breaks ordering assumptions
- Feature flag retired — previously-guarded code is now always active

**What to do:** Requires explicit testing of the affected path. Consider a staged rollout
or feature flag. Review with the team before merging.

---

### 🟡 Medium

The change affects edge case behavior, less-traveled paths, or secondary systems in ways
that are real but lower-blast-radius.

**Characteristics:**
- Behavioral change that affects a minority of users or edge cases
- Error message or user-facing copy changed (may violate documented behavior)
- Logging or metric change that could affect dashboards or alerts
- Change that behaves differently in a specific environment or config combination
- A caller whose assumption is broken, but the failure mode is visible and recoverable

**What to do:** Test the specific edge case. Notify affected teams if cross-system.
Low urgency but worth documenting.

---

### 🟢 Low

The change is isolated, cosmetic, or has a safe fallback even if behavior differs slightly.

**Characteristics:**
- Internal refactor with no behavioral difference (extract method, rename variable)
- Change confined to a module with narrow, well-tested usage
- Change where the old and new behavior are equivalent for all real inputs
- Comment, whitespace, or formatting change
- Test-only change

**What to do:** Standard review. No special verification needed beyond what the author
has already done.

---

## Escalation Rules

When in doubt, escalate. A 🟡 becomes 🟠 if:
- The affected path handles money, authentication, or PII
- The change is in a shared utility used by 5+ features
- There are no tests covering the affected behavior

A 🟠 becomes 🔴 if:
- The failure mode is silent (no error thrown, no log written, no user notification)
- The affected data is not easily recoverable
- The change affects a security or financial boundary

---

## Examples

| Change | Classification | Reason |
|--------|---------------|--------|
| `calculateTax()` now returns `0.0` instead of raising on null input | 🔴 Critical | Silent wrong value in financial calculation |
| Auth middleware now skipped for `/api/v2/*` routes | 🔴 Critical | Security boundary removed |
| `get_user()` now returns `None` instead of raising `UserNotFound` | 🟠 High | Behavioral change; callers may not null-check |
| Shared `format_date()` utility changes output format | 🟠 High | Many callers, may break display or parsing |
| `send_welcome_email()` now cc's admin | 🟡 Medium | Behavioral change, edge case, visible failure |
| Error message for invalid zip code changed | 🟡 Medium | User-facing copy changed, low blast radius |
| Variable renamed inside private method | 🟢 Low | Cosmetic, no behavioral change |
| Added null check before existing null check | 🟢 Low | Strictly defensive, no behavior change |