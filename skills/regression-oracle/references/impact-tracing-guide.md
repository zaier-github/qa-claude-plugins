# Impact Tracing Guide

How to systematically trace the downstream effects of a code change, starting from the
diff and working outward. The goal is to find what *didn't change* but will *behave differently*
because of what did.

---

## Table of Contents
1. [The Two Types of Impact](#1-the-two-types-of-impact)
2. [Tracing Call Sites](#2-tracing-call-sites)
3. [Tracing Data Contracts](#3-tracing-data-contracts)
4. [Tracing Behavioral Contracts](#4-tracing-behavioral-contracts)
5. [Tracing State Mutations](#5-tracing-state-mutations)
6. [Tracing Cross-Cutting Concerns](#6-tracing-cross-cutting-concerns)
7. [Common Regression Patterns](#7-common-regression-patterns)
8. [Git Commands for Tracing](#8-git-commands-for-tracing)

---

## 1. The Two Types of Impact

**Direct impact** — the lines that changed. The author thought about these.

**Indirect impact** — everything that depends on the changed lines' *behavior*.
This is where regressions live. The author often hasn't thought about all of these.

Your job is to systematically find indirect impact. Work outward from the changed code
in concentric rings, asking at each ring: "Does anything here depend on the old behavior?"

---

## 2. Tracing Call Sites

Who calls the modified function, method, or class? What do they assume?

**Questions to ask:**
- Does the function's signature change? (parameters added/removed/retyped, return type changed)
  If yes, find all call sites and check if they pass/use the changed parameter or return value.
- Does the function's behavior change on specific inputs? Find callers that pass those inputs.
- Does the function now throw (or stop throwing) in cases it didn't before? Find callers that
  catch that exception — or don't.
- Does the function's *side effects* change? (writes to DB, publishes an event, sends an email)
  Find code that assumes those side effects do or don't happen.

**How to find call sites (if repo is available):**
```bash
# Basic symbol search
grep -rn "function_name\|ClassName" src/ --include="*.py"

# More precise for method calls
grep -rn "\.method_name(" src/

# For JS/TS
grep -rn "import.*ModuleName\|require.*ModuleName" src/

# Git: find all files that ever imported this module
git log --all --oneline -S "function_name" -- "*.py"
```

**Red flags at call sites:**
- A caller catches a specific exception that the function no longer throws → silent failure
- A caller checks `if result is None` but the function now always returns a value → dead branch
- A caller expects a dict with certain keys but the function now returns a different shape
- A caller assumes the function is idempotent but it now has side effects (or vice versa)

---

## 3. Tracing Data Contracts

Does the change alter what data is produced, consumed, or stored?

**Questions to ask:**
- Does the function/method now return a different shape? (new keys, removed keys, type change,
  None instead of empty list, etc.)
- Does it write different data to the database? (new columns, changed formats, null values
  where there were values before)
- Does it produce a different API response shape? Are there API clients (mobile apps, partner
  integrations, frontend) that consume that shape?
- Does it change how data is serialized or deserialized? (JSON field names, date formats,
  numeric precision)
- Does it change what goes into a cache? When does that cache expire? Is stale data a risk
  during the transition?

**High-risk data contract changes:**
- Removing a field from an API response that a client reads (client will get `undefined`/`null`)
- Changing a numeric field from int to float (or vice versa) without explicit handling
- Changing a date field's timezone or format
- Removing a DB column that another service queries directly
- Changing an event payload shape that downstream consumers deserialize

---

## 4. Tracing Behavioral Contracts

Behavioral contracts are the implicit or explicit promises a piece of code makes about
*how* it behaves — not just *what* it returns.

**Questions to ask:**
- Does the change alter when or whether a side effect occurs? (email sent, event published,
  row inserted, cache invalidated)
- Does it change error handling? (swallowing exceptions, changing error types, changing
  HTTP status codes)
- Does it change timing or ordering guarantees? (sync → async, ordering of operations)
- Does it change idempotency? (can the operation now be called twice with different effects?)
- Does it change atomicity? (was a multi-step operation previously wrapped in a transaction
  that is now missing?)

**Behavioral contracts callers often rely on invisibly:**
- "This function never returns null" → callers don't null-check
- "This operation is safe to retry" → callers retry on failure
- "This always throws on invalid input" → callers catch the exception to show errors
- "This is synchronous" → callers don't handle async/await

---

## 5. Tracing State Mutations

Changes to *when* and *how* state is set can have far-reaching effects, especially in
stateful systems, long-running processes, or anything with a UI.

**Questions to ask:**
- Does the change affect when a field/variable is set, updated, or cleared?
- Is there code that reads this state later and branches based on its value?
- Does the change affect database state in a way that could conflict with existing records?
  (null constraint, unique constraint, default value change)
- Does the change affect session state, cache state, or in-memory state that persists
  across requests?
- If this is a migration or schema change: what happens to existing rows? Is a backfill needed?

---

## 6. Tracing Cross-Cutting Concerns

Some changes affect concerns that cut across the whole codebase without touching a specific
call chain.

**Logging & observability:** Does the change remove or alter log statements that monitoring
or alerting depends on? Does it change structured log fields that a dashboard queries?

**Feature flags:** Does the change interact with a feature flag? What happens in both the
enabled and disabled state? Is the flag being retired — meaning code that was previously
guarded is now always on?

**Configuration & environment:** Does the change behave differently based on env vars,
config files, or deployment environment? Is there a risk it works in staging but fails
in production due to a config difference?

**Middleware & interceptors:** Does the change bypass or alter middleware (auth, rate limiting,
logging, error handling) that wraps many routes or functions?

**Shared utilities:** Is the modified code a shared utility used across many features? If
so, every feature that uses it is a potential regression surface.

---

## 7. Common Regression Patterns

These patterns recur frequently. When you spot them in a diff, treat them as immediate
high-risk signals:

**The Quiet Return Value Change**
A function that used to throw now returns `None` (or `0`, or `[]`). Callers that relied on
the exception to handle errors will now silently proceed with a bad value.

**The Removed Guard**
A null check, bounds check, or validation that was removed as part of a "cleanup" or because
"it's not needed anymore." The assumption that it's not needed is often wrong.

**The Shared Utility Touch**
A helper function used in 15 places gets a subtle behavioral change. 14 of those places
probably still work. One doesn't.

**The Implicit Ordering Change**
Two operations that used to happen in order A→B now happen in order B→A (or concurrently).
If there's a dependency between them, it now breaks.

**The Type Coercion Swap**
A value that was a string is now an int (or vice versa). Works fine in dynamic languages
until it hits a comparison, a format string, or a serializer that cares about type.

**The Default Value Shift**
A function parameter gets a new default value. Callers that relied on the old default now
get different behavior without changing a line of their own code.

**The Exception Type Change**
An exception is changed from `ValueError` to `RuntimeError` (or from a custom exception to
a generic one). Callers that catch the specific type now miss it.

**The Transaction Boundary Move**
A DB write that was inside a transaction is moved outside it (or vice versa). In failure
scenarios, partial writes are now possible (or no longer possible).

---

## 8. Git Commands for Tracing

When the repository is available, these commands help trace impact:

```bash
# Find all files that reference a changed symbol
grep -rn "symbol_name" . --include="*.py" --include="*.js" --include="*.ts"

# Find files that import a changed module
grep -rn "from module_name import\|import module_name" . --include="*.py"

# See what else changed in the same PR/branch
git log --oneline origin/main..HEAD

# Find all callers of a function across git history
git log -S "function_name" --oneline -- "*.py"

# Check if a symbol was recently renamed (potential missed call sites)
git log --diff-filter=M --oneline -10 -- path/to/file.py

# Find test files that cover the changed code
grep -rn "function_name\|ClassName" tests/ --include="*.py" -l
```