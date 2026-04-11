# Mutation Operators Reference

A catalog of the mutation operators used by common tools, what they test, and how to
interpret surviving mutants for each operator type. Understanding what an operator *tests*
helps you quickly assess whether a survivor is signal or noise.

---

## Arithmetic Operator Replacement (AOR)

**Mutations:** `+` ↔ `-`, `*` ↔ `/`, `%` ↔ `*`, `**` ↔ `*`

**What it tests:** Whether tests verify the correct arithmetic operation.

**High-risk survivors:** Any AOR survivor in financial, scientific, or algorithmic code.
`total - discount` → `total + discount` surviving means tests don't verify that discounts
reduce the total.

**Common acquittals:** AOR in string concatenation contexts (some tools mutate `+` on
strings), AOR where both operations produce equivalent results for the input domain.

---

## Relational Operator Replacement (ROR)

**Mutations:** `>` ↔ `>=` ↔ `<` ↔ `<=` ↔ `==` ↔ `!=`

**What it tests:** Whether tests verify boundary behavior and threshold logic.

**High-risk survivors:** ROR in access control (`>=`, `<=` thresholds), rate limiting,
pricing tiers, retry counts, and any place where the exact boundary matters.

**Common acquittals:** ROR where the input domain can never produce the boundary value
(e.g., `len(items) > 0` where items is always non-empty in valid code paths — though
consider whether defensive testing is still warranted).

**Key insight:** `>` vs `>=` survivors are the most common source of real bugs. A boundary
test at exactly the threshold value is almost always the right killing test.

---

## Logical Operator Replacement (LOR)

**Mutations:** `&&`/`and` ↔ `||`/`or`, `!`/`not` removed

**What it tests:** Whether tests verify compound boolean conditions and negations.

**High-risk survivors:** LOR in auth conditions (`role == 'admin' AND active`),
validation logic (`valid_format AND valid_length`), and any compound access check.
Changing `AND` to `OR` in a permission check is a security vulnerability — if it survives,
no test verifies that *both* conditions are required.

**Common acquittals:** LOR where one operand always dominates (e.g., `True OR anything`
effectively dead-branches the second operand). Also, `NOT` mutations in code that checks
either `is_X` or `not is_X` symmetrically — if both branches are tested, the `NOT`
removal may be acquittable.

**Key insight:** Surviving `AND → OR` mutations in access control are almost always
C-DOMAIN. Treat them with highest priority.

---

## Conditional Boundary (CBS / CBR)

**Mutations:** `if (x)` → `if (true)`, `if (x)` → `if (false)`, condition replaced entirely

**What it tests:** Whether tests exercise code on both sides of a condition.

**High-risk survivors:** Any CBS where the forced-true or forced-false branch takes a
meaningfully different action. If `if (user.is_premium)` → `if (true)` survives, no test
verifies that non-premium users are denied premium behavior.

**Common acquittals:** CBS in defensive coding patterns where the branch never fires
(e.g., null guards on values that can't be null) — though flag as dead code.

---

## Return Value Mutation (RVM)

**Mutations:** `return value` → `return null`, `return 0`, `return []`, `return True/False`

**What it tests:** Whether callers verify what functions return.

**High-risk survivors:** RVM to `null`/`None` in functions whose callers don't null-check.
`return user` → `return None` surviving means callers never verify they got a real user.
Also high-risk: `return True` → `return False` in validation functions — if this survives,
no test verifies that validation actually fails invalid input.

**Common acquittals:** RVM in void functions (returning `None` from a `void` function
is equivalent). RVM in functions whose return value is explicitly discarded by all callers.

---

## Void Method Call Removal (VMR)

**Mutations:** A method call is removed entirely (for void-returning methods)

**What it tests:** Whether tests verify that side effects occur.

**High-risk survivors:** VMR on `save()`, `commit()`, `send_email()`, `publish_event()`,
`log_audit()`, `invalidate_cache()`. If removing a DB save or event publication survives,
tests don't verify the side effect happened.

**This is often the most important operator.** Silent side-effect removal is exactly how
production bugs go undetected — the function returns normally but the DB write didn't happen.

**Common acquittals:** VMR on logging calls (usually A-OBS), VMR on metrics calls where
the metric isn't part of alerting, VMR on cleanup operations in finally blocks where
leaving things uncleaned has no observable consequence.

---

## Statement Deletion (SDL)

**Mutations:** An entire statement is removed

**What it tests:** Whether every statement is necessary for some observable behavior.

**High-risk survivors:** SDL on validation statements, guard clauses, initialization
before use, or cleanup before return. If `validate_payment(amount)` can be deleted without
any test failing, no test covers invalid payment amounts.

**Common acquittals:** SDL on defensive assertions that are never triggered, redundant
assignments, pure logging statements.

---

## Constant Replacement (CR)

**Mutations:** Numeric or string constants replaced with 0, 1, -1, null, empty string

**What it tests:** Whether tests verify that the specific constant value matters.

**High-risk survivors:** CR on business-rule constants: tax rates, fee percentages,
session timeouts, rate limits, tier thresholds. `TAX_RATE = 0.08` → `TAX_RATE = 0`
surviving means no test verifies the actual tax rate is applied.

**Common acquittals:** CR on display/format constants, version strings, default values
that are always overridden by configuration.

---

## Operator and Tool Cross-Reference

| Tool | Primary operators covered | Report format |
|------|--------------------------|---------------|
| **Mutmut** (Python) | AOR, ROR, LOR, CBS, VMR, CR | Text, HTML, JSON |
| **Stryker** (JS/TS) | AOR, ROR, LOR, CBS, RVM, VMR, SDL | HTML, JSON, text |
| **PIT / Pitest** (Java) | AOR, ROR, LOR, CBS, RVM, VMR, CR | HTML, XML |
| **Cosmic Ray** (Python) | AOR, ROR, LOR, CBS, RVM, SDL | JSON, text |
| **mutmut** (Python) | AOR, ROR, LOR, CBS | Text, HTML |
| **cargo-mutants** (Rust) | RVM, VMR, CR, SDL | JSON, text |
| **infection** (PHP) | AOR, ROR, LOR, CBS, RVM, VMR | HTML, JSON, text |

See `references/tool-format-guide.md` for parsing instructions per tool.