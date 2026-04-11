# Change Type Risk Profiles

Different kinds of changes carry different inherent risk patterns. Use this guide to
calibrate your analysis based on what *type* of change you're looking at — before you
even read the diff in detail.

---

## Refactor

**Intent:** Restructure code without changing behavior.
**Inherent risk:** Medium-High. Refactors are the most common source of unintended behavioral
change, precisely because the author *intends* no change. The risk is in the gap between
"I didn't mean to change behavior" and "I actually didn't change behavior."

**Where regressions hide:**
- Extract-method refactors that subtly change execution order or scope
- Rename refactors where one call site was missed
- "Simplification" that removes a guard the author didn't realize was load-bearing
- Inlining a function that had side effects now called multiple times
- Moving code between exception handlers and accidentally changing error handling

**What to check first:** Before reading the whole diff, look for: any removed lines (not
just changed ones), any exception handling changes, any loop or conditional restructuring.

---

## Dependency Upgrade

**Intent:** Update a library to a newer version.
**Inherent risk:** Medium to Critical, highly variable. Patch versions are usually safe.
Minor versions may have behavioral changes. Major versions often break contracts.

**Where regressions hide:**
- Changed default behavior in the library (e.g., stricter validation, different date handling)
- Removed or renamed methods the codebase calls
- Changed return types or exception types
- Different behavior for edge inputs (null, empty string, 0, negative numbers)
- Changed async/sync semantics
- Security changes that affect what the library accepts or rejects

**What to check first:** Read the library's changelog between old and new version.
Look for "breaking changes" and "behavioral changes" sections. Cross-reference with
how the library is used in the codebase.

---

## Configuration Change

**Intent:** Change a setting, env var, feature flag, or infrastructure parameter.
**Inherent risk:** Low to Critical depending on what's configured. Config changes are
deceptively dangerous because the code looks unchanged.

**Where regressions hide:**
- Timeout values: too low → spurious failures; too high → cascading slowdowns
- Connection pool sizes: too small → resource exhaustion under load
- Feature flag retirement: code that was safely off is now always on
- Environment-specific config: change works in staging but production has a different value
- Rate limits: changed limits may affect downstream consumers who were calibrated to the old ones

**What to check first:** What does the changed config control? What's the blast radius
of that control? Is the new value within the safe range documented anywhere?

---

## Bug Fix

**Intent:** Correct specific incorrect behavior.
**Inherent risk:** Medium. Bug fixes are targeted, but the "bug" may have been depended
upon. Code that worked around the bug now has its workaround broken.

**Where regressions hide:**
- Callers that worked around the old incorrect behavior by compensating for it
- Tests written to assert the *buggy* behavior (they'll now fail — which is correct, but
  can be surprising if not caught)
- Cases where the "fix" overcorrects and breaks adjacent correct behavior
- Fixes that change error handling in ways that affect user-visible messages

**What to check first:** Search for any code that explicitly compensates for the behavior
being fixed. Look for comments like "// workaround for X bug" near call sites.

---

## Feature Addition

**Intent:** Add new functionality to the system.
**Inherent risk:** Low to Medium for new code paths; Medium to High when touching existing code.

**Where regressions hide:**
- Modifications to existing shared utilities or base classes to support the new feature
- New database columns or schema changes that affect existing queries
- New middleware, hooks, or interceptors that fire on existing flows
- New event listeners that fire on existing events
- Performance degradation from new queries or processing added to existing hot paths

**What to check first:** Identify every place the feature *touches existing code* (as
opposed to adding new code). Those touchpoints are where regressions live.

---

## Performance Optimization

**Intent:** Make something faster, cheaper, or more efficient.
**Inherent risk:** Medium to High. Optimizations often change execution order, caching
behavior, or trade correctness for speed in ways the author doesn't intend.

**Where regressions hide:**
- Caching: stale data served where fresh data is required; cache invalidation not updated
- Lazy loading: data that was eagerly loaded is now loaded on demand — may be missing in
  some code paths that assume it's always present
- Batching: operations that were sequential are now batched — ordering guarantees may break
- Async conversion: previously synchronous code made async — callers may not await correctly
- Index changes: queries behave differently with different indexes (edge cases, sort order)

**What to check first:** What guarantees did the original code provide that the optimized
version might not? Ordering? Freshness? Atomicity? Completeness?

---

## Security Fix / Hardening

**Intent:** Close a vulnerability or harden a security boundary.
**Inherent risk:** Medium. Security changes often tighten validation or permissions in ways
that break legitimate use cases that relied on the previously-loose behavior.

**Where regressions hide:**
- Legitimate inputs that are now rejected by stricter validation
- Internal tooling or admin flows that relied on the permission that was tightened
- API clients that relied on the endpoint being unauthenticated
- Automated systems (scripts, jobs, integrations) that are now blocked

**What to check first:** What was previously allowed that is now blocked? Are there any
known legitimate uses of the thing being locked down?

---

## Database Migration

**Intent:** Alter the database schema or data.
**Inherent risk:** High to Critical. Schema changes are permanent and affect live data.

**Where regressions hide:**
- Removed columns still queried by code (query will fail or return null)
- Renamed columns where the rename isn't reflected everywhere
- Type changes that cause implicit coercion issues or break ORM mappings
- Added NOT NULL constraints without a default for existing rows
- Changed defaults that affect newly-inserted rows in unexpected ways
- Missing index that causes previously-fast queries to become slow

**What to check first:** Is the migration reversible? What's the rollback plan?
Does the application code deploy atomically with the migration, or is there a window
where old code runs against the new schema (or vice versa)?