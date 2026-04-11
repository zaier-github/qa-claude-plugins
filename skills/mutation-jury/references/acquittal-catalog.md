# Acquittal Catalog

A taxonomy of surviving mutants that typically don't represent genuine test gaps.
Use this during the quick acquittal sweep (Step 1) to efficiently dismiss noise before
spending deliberation time on real findings.

Each category includes: what it looks like, why it's acquittable, and the exceptions
that override the acquittal — because every category has edge cases worth catching.

---

## Category 1: Equivalent Mutants

**What they are:** Mutations that produce code that is semantically identical to the
original — no input can produce a different output. The test suite *can't* kill them
because there's nothing different to observe.

**Common examples:**
- `x = x + 1` → `x += 1` (same semantics in most languages)
- `return a == b` → `return !(a != b)` (logically identical)
- Changing `True` → `not False` or `1 != 0`
- Reordering commutative operations: `a + b` → `b + a`
- Changing `len(lst) == 0` → `not lst` (equivalent in Python)
- Removing a double negation: `!!x` → `x`

**Acquittal reason:** `EQUIVALENT — no observable behavioral difference`

**Exceptions:** Floating-point arithmetic is not always commutative. `a + b` and `b + a`
can produce different results with IEEE 754. In financial or scientific code, don't
auto-acquit commutative reorderings.

---

## Category 2: Boundary Arithmetic Noise

**What they are:** Off-by-one mutations in boundary comparisons where both sides of
the boundary produce equivalent *practical* behavior for the application's inputs.

**Common examples:**
- Changing `array.length - 1` → `array.length` in an index calculation where the
  array is always non-empty and the loop always terminates before the last element
- Changing a pagination `LIMIT 10` → `LIMIT 11` where results are always well under 10
- Off-by-one in a retry count (retry 3 vs 4 times) where both are acceptable

**Acquittal reason:** `BOUNDARY NOISE — both values produce equivalent practical behavior`

**Exceptions — convict instead:**
- Any boundary mutation in financial calculations (prices, quantities, fees)
- Index mutations that could produce out-of-bounds access
- Off-by-one in security-sensitive counts (max login attempts, rate limit thresholds)
- Retry/timeout counts where the boundary matters for user experience

---

## Category 3: String and Message Content Mutations

**What they are:** Mutations to string literals — error messages, log strings, display
text, labels — that don't affect program logic.

**Common examples:**
- `"User not found"` → `""` in an exception message
- `logger.info("Processing payment")` → `logger.info("")`
- Changing a UI label string
- Mutating a format string's static text portions

**Acquittal reason:** `STRING CONTENT — message text doesn't affect logic`

**Exceptions — convict instead:**
- String mutations in code where the *content* drives behavior: regex patterns,
  SQL queries, API endpoint paths, config keys, dictionary/map keys
- Error messages that are parsed by callers or monitoring systems
- Strings that are asserted in tests (the mutation *should* be killed — if it isn't,
  the test assertion is too loose)
- User-facing messages in compliance or legal contexts where wording matters

---

## Category 4: Dead Code Mutations

**What they are:** Mutations in code that is unreachable given the application's
current input space — code after unconditional returns, in conditions that can never
be true, or in deprecated code paths.

**Common examples:**
- Code after `return`, `throw`, `panic`, `exit` in a function body
- Conditions like `if (false)` or `if (x < 0)` where `x` is always non-negative
- Mutations in `else` branches of conditions that are always true
- Mutations in code that's only reachable via a removed feature flag

**Acquittal reason:** `DEAD CODE — unreachable under current inputs`

**Exceptions:** If the code *should* be reachable but isn't (e.g., defensive programming
that was never triggered), the lack of a test is itself a signal worth noting — flag
with `DEFER — dead code that may be intended as a safety net`.

---

## Category 5: Test Infrastructure Mutations

**What they are:** Mutations in test helpers, fixtures, factories, mocks, or test
utilities that survive because the test suite doesn't test its own infrastructure.

**Common examples:**
- Mutations in `factories/user_factory.py` or `fixtures/order.json`
- Mutations in mock implementations of services
- Mutations in `conftest.py` setup/teardown helpers
- Mutations in test assertion helper functions

**Acquittal reason:** `TEST INFRASTRUCTURE — not application logic`

**Exceptions:** Test utilities that are also used in production code (e.g., a validation
helper that lives in a `utils/` module and is imported in both tests and production) should
be treated as production code and deliberated individually.

---

## Category 6: Logging and Observability Mutations

**What they are:** Mutations to logging calls, metrics emissions, trace spans, or
debugging instrumentation where the logged data doesn't affect application behavior.

**Common examples:**
- `log.error("Payment failed", error=e)` → `log.error("Payment failed")`
- `metrics.increment("checkout.complete")` → removed entirely
- `span.set_attribute("user_id", user.id)` → `span.set_attribute("user_id", "")`

**Acquittal reason:** `OBSERVABILITY ONLY — no effect on application behavior`

**Exceptions — convict instead:**
- Log mutations where the log output is tested (the test should be killing this)
- Mutations that remove error logging in paths where silent failures are high-risk
  (flag as `DEFER — silent failure risk if logging removed`)
- Metrics mutations in code where metric-based alerting is the primary failure detection
  mechanism (removing this metric removes your early warning system)

---

## Category 7: Trivial Constant Mutations

**What they are:** Mutations to constants or literal values that have no meaningful
semantic consequence.

**Common examples:**
- Changing a string constant used only for display: `VERSION = "1.0"` → `VERSION = ""`
- Changing a comment (some tools mutate these)
- Mutations to values that are overridden immediately after assignment
- Mutations in configuration defaults that are always overridden by environment variables

**Acquittal reason:** `TRIVIAL CONSTANT — value has no semantic consequence`

**Exceptions:** Constants that represent business rules, limits, or thresholds (e.g.,
`MAX_RETRIES = 3`, `FREE_TIER_LIMIT = 1000`, `SESSION_TIMEOUT_MINUTES = 30`) are
never trivial — mutations to these should be deliberated.

---

## Using the catalog efficiently

During the quick acquittal sweep, scan the full survivor list and group mutants into
these categories *before* any individual deliberation. A well-run sweep should acquit
30–60% of surviving mutants in most mutation reports — leaving a much smaller, higher-signal
set for genuine deliberation.

Document the sweep results honestly:
```
Quick acquittal sweep: 47 of 112 survivors acquitted
- Equivalent: 12
- String/message: 18
- Dead code: 8
- Test infrastructure: 5
- Trivial constants: 4
```

This accounting builds trust that the jury isn't hiding inconvenient findings — it's
efficiently separating signal from noise.