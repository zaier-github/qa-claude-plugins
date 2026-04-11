# Domain Coverage Targets

Recommended coverage standards by domain type. These are starting points for the
"What Good Looks Like" section of the Risk Map — adapt to the team's context and
risk tolerance.

The key principle: coverage targets should reflect the *cost of a silent bug* in that
domain, not just effort to achieve them.

---

## Tier 1: Zero-tolerance domains (target: ≥90% line, ≥85% branch)

These domains handle irreversible, high-stakes operations where a silent bug has
serious consequences. Every conditional path should be tested.

- **Payments, billing, subscriptions, refunds** — incorrect charges or missed refunds
  have financial and trust consequences
- **Authentication and session management** — a gap here is a security vulnerability
- **Authorization and access control** — untested permission logic means data leakage
- **Data migrations** — untested migrations run on production data with no undo
- **Regulatory compliance logic** — GDPR deletion, HIPAA audit trails, PCI scope

**Branch coverage matters most here.** A payment function with 95% line coverage but
30% branch coverage is not acceptably tested — the branches are where the edge cases live.

---

## Tier 2: Core business logic (target: ≥80% line, ≥70% branch)

The primary logic that makes the product work. Bugs here are user-visible and frequent
support tickets.

- **Core domain models and their behaviors** — the objects that represent the product's
  core concepts (orders, users, products, posts, whatever the product primarily manages)
- **Business rules engine** — pricing rules, eligibility logic, workflow transitions
- **Core API handlers** — the endpoints that external clients depend on
- **Data transformation and import/export** — especially if downstream systems consume it

---

## Tier 3: Supporting flows (target: ≥70% line, ≥55% branch)

Important but lower-blast-radius. Bugs are visible but often recoverable or affect a
subset of users.

- **User notifications** (email, SMS, push) — bugs are annoying but rarely catastrophic
- **Search and filtering** — wrong results are bad UX but not data loss
- **Reporting and analytics** — incorrect numbers in dashboards matter but don't corrupt source data
- **Integration adapters** — third-party API wrappers where the third-party handles the
  critical logic and you're mostly marshaling data

---

## Tier 4: Utilities and infrastructure (target: ≥50% line, ≥40% branch)

Supporting code that serves other code. Typically tested implicitly through the code
that calls it, but benefits from direct tests on edge cases.

- **String formatting, date handling, number formatting utilities**
- **Logging and observability helpers**
- **Configuration loading and environment parsing**
- **Generic data structure utilities**

---

## Tier 5: Internal tooling and scripts (target: ≥30% line)

Used by developers, not end users. Failures are visible immediately and rarely silent.
Lower bar is acceptable, but critical scripts (deployment, migration, data repair)
should be at Tier 2 standards regardless.

- **CLI tools and administrative scripts**
- **Development utilities and generators**
- **One-off data scripts** (these often have *no* tests — document them and note
  that they should be treated as Tier 2 before running on production data)

---

## Special cases

**Legacy moat code:** Start lower — even 40% coverage on legacy code that was at 0%
is a meaningful improvement. The goal is to build *enough* of a safety net to begin
refactoring safely, not to achieve ideal coverage before touching it.

**External-facing APIs (public or partner):** Treat as Tier 2 minimum, regardless of
the domain's general tier. Contract breaks with external consumers are high-cost.

**Recently-added modules:** New code should start at Tier 2 or above. It's much easier
to maintain coverage discipline from the start than to retrofit it onto 10,000 lines.

**Code with active incidents:** Promote the affected module to Tier 1 standards
immediately after the incident. The bug already proved the coverage gap has teeth.