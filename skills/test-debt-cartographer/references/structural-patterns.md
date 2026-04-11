# Structural Patterns

A catalog of systemic test debt patterns — configurations of coverage gaps that signal
deeper architectural or process problems. Finding these is often more valuable than any
individual gap, because they explain *why* the gaps exist and what would fix them structurally.

---

## Pattern 1: The Legacy Moat

**What it looks like:** A cluster of old, large, complex files with very low coverage, high
churn, and often many TODO/FIXME comments. Usually found in the oldest part of the codebase.
The team knows it's risky but nobody wants to touch it — which is exactly why nobody has
written tests for it.

**Why it's dangerous:** These files are often load-bearing. They accumulated complexity
because they kept getting new requirements. They're hard to test because they're hard to
understand. And they keep changing — which means they keep breaking.

**Signal:** Files that are simultaneously in the oldest 20% by creation date AND the
top 20% by recent commits AND below 30% coverage.

**What to recommend:** Don't try to cover the whole moat at once. Identify the 2–3 most-called
functions and write characterization tests — tests that document current behavior rather
than asserted-correct behavior. This gives a safety net for refactoring.

---

## Pattern 2: Coverage Theater

**What it looks like:** Line coverage looks healthy (70%+) but branch coverage is very low
(30% or below). Tests execute most lines but don't verify that the code behaves correctly
under different conditions.

**Why it's dangerous:** A test that calls `apply_discount(cart, coupon)` with valid inputs
covers the lines but doesn't test: what if coupon is null? What if cart is empty? What if
the discount exceeds the total? The code looks tested; the bugs are hiding in the branches.

**Signal:** File-level line coverage > 60% AND branch coverage < 40%. Or: many test files
with a single test function per tested function (suggests "happy path only" test writing).

**What to recommend:** Audit the highest-risk files for branch coverage specifically. Add
tests for every conditional path: null inputs, boundary values, error conditions, and
permission edge cases.

---

## Pattern 3: The Untested Integration Seam

**What it looks like:** Individual modules have reasonable unit test coverage, but the
interfaces *between* them are never tested. Module A is 80% covered, Module B is 75% covered,
but nothing tests what happens when A calls B with real data.

**Why it's dangerous:** Most production bugs are integration bugs. The units work correctly
in isolation; they fail at the boundary. Contract mismatches, unexpected null values, format
differences, and async timing issues all live at integration seams.

**Signal:** Good unit coverage across modules, but sparse or absent integration/contract tests.
Look especially at: service-to-service calls, ORM-to-database interactions, third-party API
wrappers, and event publisher/consumer pairs.

**What to recommend:** Write integration tests that exercise real data flowing across the
seam. Don't mock the boundary you're testing — that defeats the purpose.

---

## Pattern 4: The Domain Blind Spot

**What it looks like:** An entire business domain — a subdirectory, a service, a logical
module — has consistently low coverage across all its files. It's not that coverage is
uneven; it's that an entire area was never prioritized for testing.

**Why it's dangerous:** Domain blind spots often correspond to "the thing we don't touch
often" — which makes the gap feel acceptable. But when something does change in that domain
(a new requirement, a bug fix, a dependency upgrade), there's no net to catch regressions.

**Signal:** A subdirectory or module where average coverage is below 25% across all files,
and no files are above 50%.

**What to recommend:** Treat the domain as a mini-project. Pick the 3 most-called entry
points and write integration tests from the outside in. Don't try to unit-test every class
immediately — establish an outer layer of confidence first.

---

## Pattern 5: The Untested Critical Path

**What it looks like:** The single most important user-facing flow — signup, purchase,
core action — has no end-to-end test. Individual components may be tested, but nobody
has written a test that walks through the entire flow as a user would.

**Why it's dangerous:** End-to-end critical path failures are the most visible and
damaging bugs. They affect every user. And because the components are tested individually,
the team may have false confidence that "it's all tested."

**Signal:** No E2E or integration test file that references the main entry point of the
product's core flow. Or: E2E tests exist but only cover the happy path with no variation.

**What to recommend:** Write one end-to-end smoke test for the critical path immediately.
It doesn't have to be comprehensive — a single test that exercises the full flow end-to-end
provides enormous value and catches integration breaks that unit tests miss.

---

## Pattern 6: The Orphaned Test Suite

**What it looks like:** Test files exist but they're testing code that has since been
refactored, renamed, or removed. The tests pass, but they're not covering what the team
thinks they're covering.

**Why it's dangerous:** It creates false confidence. Teams assume coverage is higher than
it is because the test count looks healthy. Often discovered when a real bug slips through
code that "has tests."

**Signal:** Test files that import symbols that no longer exist in their expected location.
Or test files that haven't been modified in 12+ months while their corresponding source
files have changed significantly.
```bash
# Find test files older than their source files (rough signal)
git log --oneline -1 -- tests/test_module.py   # last test change
git log --oneline -1 -- src/module.py           # last source change
```

**What to recommend:** Audit test files for import health. Run coverage with
`--fail-under=0` and verify that tests are actually executing the current code,
not stale copies or renamed symbols.

---

## Pattern 7: The Exception Graveyard

**What it looks like:** Error handling code — `except` blocks, `catch` clauses,
`rescue` statements — is systematically untested. The happy paths are covered but
every failure mode is a black box.

**Why it's dangerous:** Exceptions and error paths are exactly what fires in production.
An untested `except Exception as e: pass` is a silent bug waiting to happen. Untested
error handling means the team doesn't know if errors are logged, surfaced to users,
retried, or just swallowed.

**Signal:** Branch coverage analysis shows that `except`/`catch` branches are consistently
uncovered. Or: grep for exception handlers and cross-reference with test files that test
those scenarios.

**What to recommend:** For each critical code path, add at least one test that exercises
the failure mode — what happens when the database is unavailable, the API returns a 500,
the input is malformed, or the operation times out.