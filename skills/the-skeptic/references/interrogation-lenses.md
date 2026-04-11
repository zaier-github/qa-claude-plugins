# Interrogation Lenses

A catalog of thinking lenses for interrogating a spec. Under each lens, example questions
are provided to prime your thinking — but don't treat these as a checklist to mechanically
tick off. Use them as a warm-up. The best questions are the ones specific to *this* spec.

---

## 1. Actor & Permission Boundaries

Who are all the actors involved? What can each one do — and critically, what are they
*not* allowed to do? Specs often define the happy path for one actor and leave everyone
else undefined.

**Starter questions:**
- Who are all the roles that interact with this feature? (admin, owner, viewer, guest, API caller, support agent, etc.)
- Can an actor perform this action on behalf of another? (impersonation, delegation, proxies)
- What happens when a user's role changes mid-flow? (e.g., downgraded from admin while editing)
- Are there org-level vs. user-level permissions? Do they conflict?
- What does an unauthenticated user see or receive?
- Can one actor undo or override another actor's action?
- Is there a "super admin" path not mentioned that could bypass normal rules?

---

## 2. State & Lifecycle

Every entity and every flow has states. Specs often only describe the main path from
start to finish and skip the messy middle, the paused states, and what happens at the end.

**Starter questions:**
- What are *all* the states this object/flow can be in? (draft, pending, active, paused, cancelled, expired, archived, deleted...)
- What transitions are valid between states? What transitions are *invalid* and what happens if attempted?
- Can a user re-enter a flow they already completed?
- What happens to related objects when this one changes state? (e.g., cancel an order — what happens to its line items, invoices, notifications?)
- Is there a "zombie" state — something that gets stuck and nobody knows what to do with it?
- Does anything expire? What triggers expiry? What happens on expiry?
- Is soft delete different from hard delete? Which is used here?

---

## 3. Edge & Boundary Conditions

The spec probably assumes "normal" input and behavior. What happens at the edges?

**Starter questions:**
- What's the minimum valid input? The maximum?
- What if a required field is empty, null, whitespace-only, or zero?
- What if a list has zero items? One item? The maximum number of items?
- What if a date is in the past? In the far future? Today at midnight in a different timezone?
- What if a monetary value is exactly $0? Negative? Fractional cents?
- What if a string contains special characters, emoji, or extremely long content?
- What if the same request is submitted twice in quick succession?

---

## 4. Error & Failure Paths

Specs love to describe what happens when everything goes right. They rarely describe
what happens when it doesn't.

**Starter questions:**
- What happens if a required downstream service is unavailable?
- What happens if a third-party API call times out or returns an unexpected response?
- If a multi-step flow partially completes and then fails, what's the rollback behavior?
- Are errors surfaced to the user? In what form? (toast, inline, modal, email?)
- Are errors logged? Are they alerted on? Who gets alerted?
- What's the retry behavior? Is the action idempotent?
- What does the user see if they're offline or lose connection mid-flow?
- Is there a graceful degradation path, or does the whole feature break?

---

## 5. Concurrency & Timing

Specs are usually written as if one thing happens at a time. In production, it's never one thing.

**Starter questions:**
- What if two users edit the same record simultaneously? Last write wins? Conflict resolution?
- What if a user triggers this action twice before the first one completes?
- What if a background job and a user action affect the same data at the same time?
- Are there race conditions in the state machine? (e.g., can an item transition to two states at once?)
- What if a scheduled job runs while a user is mid-flow?
- Is there a lock, queue, or mutex implied but not specified?
- What are the ordering guarantees on events or notifications?

---

## 6. Data Integrity & Validation

Where does data come from? What form is it in? What's considered valid?

**Starter questions:**
- What is the canonical source of truth for each piece of data in this flow?
- What input validation is required? Server-side, client-side, or both?
- Is there a risk of duplicate records being created? What prevents it?
- Are there cascading consequences if referenced data is modified or deleted?
- What happens to existing data if the schema changes (migration, backfill, null-handling)?
- Are there format constraints not mentioned? (phone numbers, postal codes, currency precision)
- What encoding is assumed? (UTF-8? ASCII-safe? HTML-safe?)

---

## 7. Integration & Dependencies

Features rarely live in isolation. What does this touch that the spec doesn't mention?

**Starter questions:**
- What other internal systems does this feature read from or write to?
- What third-party services does it depend on? (payments, email, SMS, analytics, auth providers)
- Does this feature produce events that other systems consume? Are those consumers affected by this change?
- Are there webhooks, callbacks, or async notifications implied?
- Does this change any APIs that external partners or clients consume?
- Are there mobile apps, browser extensions, or other clients that need to be updated in sync?
- Does this touch shared infrastructure (queues, caches, CDNs) in ways not specified?

---

## 8. Reversibility & Undo

Can users change their minds? Can admins fix mistakes?

**Starter questions:**
- Is this action reversible? If yes, how? If no, is the user warned before confirming?
- Is there an undo window? How long? What triggers it to close?
- Can an admin reverse or override a user's action?
- What happens to downstream effects if an action is reversed? (e.g., cancel a payment — what about the fulfillment that already started?)
- Is there an audit trail? Can past states be reconstructed?
- What happens if a reversal fails partway through?

---

## 9. Performance & Scale

Does the spec hold up when used heavily, at volume, or under stress?

**Starter questions:**
- Are there any unbounded queries, lists, or loops? What's the pagination strategy?
- What's the expected volume of this operation per day/hour? Is that handled?
- Are there any operations that could become slow at scale (e.g., counting across millions of rows)?
- Is caching involved? When does the cache invalidate? What happens with stale data?
- Are there rate limits on actions? Are they specified?
- What's the SLA for this feature? Is there a degraded-mode fallback?
- Are there bulk operations? What's the limit on batch size?

---

## 10. Security & Abuse

How could a bad actor misuse this feature, intentionally or accidentally?

**Starter questions:**
- Can a user access or modify another user's data by manipulating IDs or URLs?
- Is any user-supplied content rendered as HTML? Is it sanitized?
- Are there API endpoints implied that need authentication/authorization checks?
- Could this feature be abused to enumerate users, resources, or sensitive data?
- Are there rate limits to prevent abuse (signup flooding, brute force, scraping)?
- Does this feature expose PII? Is it logged? Is the log access-controlled?
- Are there CSRF or replay attack vectors?
- Is there a privilege escalation path hidden in the state transitions?

---

## 11. Observability & Auditability

How will the team know if this is broken, slow, or being abused?

**Starter questions:**
- What metrics will tell us this feature is healthy? Are they being instrumented?
- What should be logged? At what level? (info, warn, error)
- Is there an audit log of who did what and when? Who can access it?
- Are there alerts for anomalies (error rate spikes, unexpected state transitions)?
- How will support staff investigate a user complaint about this feature?
- Is there tracing/correlation across the services this touches?

---

## 12. UX & Communication

What does the user actually see and read in every scenario?

**Starter questions:**
- What copy is shown in the error states? Is it written?
- Are there empty states? What does the user see if there's no data yet?
- Are there loading states? What if loading takes a long time?
- What confirmation or success messaging is shown after key actions?
- Are there emails, push notifications, or in-app notifications triggered? Is the copy written?
- Is the feature accessible? (keyboard navigable, screen reader compatible, color contrast)
- Are there locale/language/currency considerations for international users?
- What does the experience look like on mobile vs. desktop?

---

## 13. Regulatory & Compliance

Are there legal, policy, or contractual constraints implied but not stated?

**Starter questions:**
- Does this feature handle personal data subject to GDPR, CCPA, or other privacy laws?
- Are there data retention requirements? Data deletion requirements?
- Are there financial regulations that apply? (PCI-DSS, SOX, KYC/AML)
- Are there contractual commitments to enterprise customers that this might affect?
- Are there accessibility requirements (WCAG, ADA) that apply?
- Is there a need for a paper trail for legal or audit purposes?
- Does this feature affect minors? Are there age-gating requirements?