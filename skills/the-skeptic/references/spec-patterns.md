# Spec Anti-Patterns

A catalog of common patterns in poorly-written or under-specified feature specs, and what
each one typically hides. Use this as a diagnostic aid — when you see a pattern, dig there.

---

## "The Happy Path Only"

**What it looks like:** The spec walks through one scenario end-to-end with no branching.
Every step works. The user clicks the button, the thing happens.

**What it hides:** Error paths, retry logic, partial failures, what happens when a dependency
is unavailable, what the user sees in every failure mode.

**Dig here:** Phase 4 (Error & Failure Paths), Phase 5 (Concurrency), Phase 7 (Integrations)

---

## "It Should Work Like [Other Product]"

**What it looks like:** "This works like Stripe's coupon system" or "similar to how Slack
handles notifications."

**What it hides:** The reference product has years of edge case handling that the spec author
hasn't explicitly opted into. Which behaviors are being adopted? Which aren't? What happens
when user expectations from the reference product aren't met?

**Dig here:** Phase 3 (Boundary Conditions), Phase 12 (UX & Communication), Phase 2 (State)

---

## "The Passive Voice Spec"

**What it looks like:** "Users will be notified." "The order will be cancelled." "Access will
be revoked."

**What it hides:** Who does the thing? When exactly? Under what conditions? What triggers it?
What system is responsible? The passive voice hides agency and causality.

**Dig here:** Phase 1 (Actor & Permissions), Phase 7 (Integrations), Phase 2 (State & Lifecycle)

---

## "The Implicit Admin"

**What it looks like:** The spec describes the user flow but never mentions what admins can
do, see, or override.

**What it hides:** Admin capabilities (or lack thereof) for supporting users, fixing data
issues, managing abuse, reviewing audit trails, or handling edge cases that users can't
resolve themselves.

**Dig here:** Phase 1 (Actor & Permissions), Phase 11 (Observability), Phase 8 (Reversibility)

---

## "TBD / To Be Designed"

**What it looks like:** "Error copy TBD", "exact validation rules TBD", "edge case behavior
to be determined in implementation."

**What it hides:** Explicit acknowledgment that the spec is incomplete — but these gaps
are sometimes treated as minor when they're actually load-bearing. "TBD" near a security
check or a financial calculation is a red flag.

**Dig here:** Wherever the TBD lives — treat it as a 🔴 if in a sensitive area, 🟡 otherwise.

---

## "The Assumed Integration"

**What it looks like:** "Send the user a confirmation email." "Log this to our analytics
system." "Update the user's billing."

**What it hides:** Which system handles this? What does it need from this feature? What
happens if it's unavailable? Who owns the contract? Is it synchronous or async?

**Dig here:** Phase 7 (Integration & Dependencies), Phase 4 (Error Paths), Phase 5 (Concurrency)

---

## "The Eternal Present Tense"

**What it looks like:** Specs written as if the system has no history. "The user clicks
Delete and the item is deleted." But what about items that were in flight? Items with
dependencies? Items that were deleted and recreated?

**What it hides:** Lifecycle transitions, cascading effects, and what happens to data that
was created under old rules when new rules apply.

**Dig here:** Phase 2 (State & Lifecycle), Phase 8 (Reversibility), Phase 6 (Data Integrity)

---

## "One Role, One World"

**What it looks like:** The spec describes behavior for one user type (usually the primary
persona) and doesn't mention others.

**What it hides:** Permission conflicts, multi-tenant behavior, org vs. user scope,
what read-only users see, what happens in shared contexts (shared dashboards, team resources).

**Dig here:** Phase 1 (Actor & Permissions), Phase 10 (Security & Abuse)

---

## "The Magic Button"

**What it looks like:** "The user clicks Submit and everything is saved." No mention of
validation, what "saved" means transactionally, latency, or confirmation.

**What it hides:** Validation rules, transaction boundaries, loading states, success
confirmation, what happens if the save partially succeeds.

**Dig here:** Phase 6 (Data Integrity), Phase 3 (Boundary Conditions), Phase 12 (UX)

---

## "Scale? What Scale?"

**What it looks like:** The spec is written for a single user, single record, single event.
No mention of what happens at volume.

**What it hides:** N+1 query risks, list pagination, rate limits, bulk operation handling,
background job behavior under load, what happens when a report runs across 10M records.

**Dig here:** Phase 9 (Performance & Scale), Phase 5 (Concurrency)

---

## "Obvious Default"

**What it looks like:** "The system will handle edge cases sensibly." Or behavior in an
edge case is never mentioned because it "seems obvious."

**What it hides:** Two developers will implement "sensible" differently. What's obvious to
the spec author isn't obvious to the implementor, the QA engineer, or the support agent
trying to explain behavior to a user six months later.

**Dig here:** Anywhere the spec is silent — silence is an assumption, not a guarantee.