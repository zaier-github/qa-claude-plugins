# Verdict Guide

The deliberation framework for individual surviving mutants. Use this during Step 2
(individual deliberation) after the quick acquittal sweep has cleared obvious noise.

---

## The Three Verdicts

### Convict 🔴

The mutation reveals a genuine gap in test coverage. The mutated code *could* produce
incorrect behavior that matters, and no test currently catches it.

Conviction means: recommend writing a test. Include the specific killing test prescription.

**Conviction reasons** — use the most specific applicable reason:

| Code | Reason | What it means |
|------|--------|---------------|
| `C-LOGIC` | Logic gap | The mutation changes a decision outcome and tests don't verify that outcome |
| `C-BOUNDARY` | Boundary gap | A boundary condition is untested — the mutation crosses it undetected |
| `C-ERROR` | Error path gap | The mutation changes error/exception behavior and no test exercises the error path |
| `C-CONTRACT` | Contract gap | The mutation changes what the function returns/does in a way callers depend on |
| `C-DOMAIN` | Domain logic gap | The mutation changes business-critical behavior (financial, auth, compliance) |
| `C-INTEGRATION` | Integration gap | The mutation changes behavior at a seam between components with no integration test |
| `C-SIDE-EFFECT` | Side effect gap | The mutation removes or alters a side effect (DB write, event publish) no test verifies |

---

### Acquit ✅

The mutant is harmless — equivalent, trivial, in dead code, or otherwise not worth testing.

Acquittal reasons from the acquittal catalog:

| Code | Reason |
|------|--------|
| `A-EQUIV` | Equivalent mutant — semantically identical behavior |
| `A-NOISE` | Boundary arithmetic noise — both sides equivalent in practice |
| `A-STRING` | String/message content — no logic effect |
| `A-DEAD` | Dead code — unreachable under current inputs |
| `A-INFRA` | Test infrastructure — not application logic |
| `A-OBS` | Observability only — logging/metrics with no behavior effect |
| `A-CONST` | Trivial constant — value has no semantic consequence |

---

### Defer ⚖️

The verdict is genuinely ambiguous. The mutation *might* matter or *might not* — the
answer depends on requirements, domain context, or system behavior that can't be
determined from the code alone.

**When to defer:**
- The mutation changes behavior that *could* be intentional or *could* be a bug,
  and you can't tell which without knowing the product requirements
- The mutation is in code that appears to be dead but might be a safety net — needs
  a domain expert to confirm
- The mutation changes behavior that matters only in a specific deployment configuration
  that isn't documented in the code
- The mutation is in a logging/observability path where whether it matters depends on
  whether alerting is configured against that specific signal

**Defer format:** State the specific question that needs to be answered:
> "Is it intended that `apply_discount()` silently returns the original price when given
> an invalid coupon, or should it raise? If it should raise, this is C-CONTRACT. If
> silent fallback is intended, this is A-EQUIV."

---

## Deliberation questions

For each non-acquitted mutant, work through these:

**1. What does the original code do?**
Understand the intent of the original line before you look at the mutation. What is
this code trying to accomplish in the context of the function?

**2. What does the mutation do differently?**
Be specific. "Changes `>` to `>=`" isn't enough — explain the behavioral consequence:
"An input exactly equal to the threshold now takes the `else` branch instead of the
`if` branch. Is there a test that sends exactly-threshold input?"

**3. Can any real input trigger this difference?**
If no real input can produce different behavior between the original and the mutation,
it's equivalent → acquit. If the difference requires a contrived input that never
occurs in practice, consider acquitting with a note.

**4. What breaks if the mutation is the "true" version?**
Think about production consequences. A mutation that changes `>=` to `>` in a discount
threshold function means some users get the discount they shouldn't, or don't get it
when they should. Is that important?

**5. Should a test catch this?**
Even if the mutation is detectable, maybe there's a good reason no test catches it
(the behavior is explicitly undefined, it's a known acceptable ambiguity). Be honest
about this rather than defaulting to conviction.

---

## Worked examples

**Example 1 — Conviction (C-BOUNDARY)**

Original: `if (attempts >= MAX_LOGIN_ATTEMPTS):`
Mutation: `if (attempts > MAX_LOGIN_ATTEMPTS):`

Deliberation: With the mutation, a user who has made exactly `MAX_LOGIN_ATTEMPTS` failed
logins does not get locked out — they get one free extra attempt. No test sends exactly
`MAX_LOGIN_ATTEMPTS` failed attempts and verifies the lockout behavior.

Verdict: **Convict — C-BOUNDARY** (security-sensitive boundary, no boundary test)
Killing test: "Test that a user is locked out after exactly `MAX_LOGIN_ATTEMPTS` failed
attempts, not after `MAX_LOGIN_ATTEMPTS + 1`."

---

**Example 2 — Acquittal (A-STRING)**

Original: `raise ValueError("Coupon code cannot be empty")`
Mutation: `raise ValueError("")`

Deliberation: The mutation changes the error message text but not the exception type or
the fact that an exception is raised. Callers catch `ValueError`; the message is for
humans reading logs, not for program logic.

Verdict: **Acquit — A-STRING** (message content, no logic effect)
*Exception check:* Is this message parsed anywhere? Is it asserted in tests? No → acquit.

---

**Example 3 — Defer**

Original: `if (user.role == 'admin' or user.is_superuser):`
Mutation: `if (user.role == 'admin'):`

Deliberation: The mutation removes the `is_superuser` check. Does `is_superuser` represent
a real permission tier with distinct behavior, or is it always true for admins and redundant?
If the former, this is C-DOMAIN (a real security gap). If the latter, A-EQUIV.

Verdict: **Defer** — "Is `is_superuser` always equivalent to `role == 'admin'` in this
system, or are there users where `is_superuser=True` but `role != 'admin'`? If the latter,
this is a security gap — convict as C-DOMAIN."