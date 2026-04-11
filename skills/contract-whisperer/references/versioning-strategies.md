# Versioning Strategies

When a breaking change is unavoidable, the question becomes: how do we ship it safely?
This reference covers the main strategies, when each applies, and the tradeoffs.

---

## Strategy 1: Additive Evolution (Expand / Contract)

**When to use:** You can express the new behavior alongside the old for a transition period.

**How it works:**
1. **Expand**: Add new fields/behavior *alongside* old ones. Both exist simultaneously.
2. **Notify**: Communicate to consumers that the old form is deprecated and the new form
   should be used. Set a sunset date.
3. **Contract**: After consumers have migrated (or the sunset date passes), remove the old form.

**Example:** Renaming `amount` to `total_amount`:
- Phase 1: Return both `amount` and `total_amount` in the response
- Phase 2: Document `amount` as deprecated (`deprecated: true` in OpenAPI, `@deprecated` in GraphQL)
- Phase 3: Remove `amount` after migration window

**Best for:** Field renames, schema restructuring, type additions
**Not suitable for:** Security changes that require immediate removal of old behavior

---

## Strategy 2: URI Versioning

**When to use:** A large set of breaking changes makes additive evolution impractical.
You need to publish a clean break.

**How it works:**
- Publish new API at a new path: `/api/v2/payments` alongside `/api/v1/payments`
- Both versions run simultaneously until v1 is sunset
- Consumers migrate on their own timeline within the sunset window

**Variants:**
- Path versioning: `/v2/` (most common, easiest to route)
- Header versioning: `API-Version: 2024-01-15` (cleaner URLs, harder to test in browser)
- Query parameter: `?version=2` (simple but pollutes query space)

**Best for:** Major API redesigns, many simultaneous breaking changes
**Tradeoffs:** Maintaining two versions is expensive; must set and enforce sunset dates

---

## Strategy 3: Schema / Content Negotiation

**When to use:** Clients can signal which version of a response they want.

**How it works:**
- Client sends `Accept: application/vnd.myapi.v2+json`
- Server returns v1 or v2 response based on the header
- Default (no header) returns older version for backwards compatibility

**Best for:** Response schema evolution where the underlying data is the same
**Tradeoffs:** Requires clients to opt in; server logic becomes more complex

---

## Strategy 4: Feature Flags / Gradual Rollout

**When to use:** You want to test the new behavior with a subset of consumers before
full rollout, or you need an emergency rollback path.

**How it works:**
- New behavior is behind a feature flag, enabled per-consumer or per-account
- Internal consumers and partners are migrated incrementally
- Flag is removed when all consumers are on new behavior

**Best for:** Behavioral contract changes, high-risk schema changes with known consumers
**Not suitable for:** Public APIs with many unknown consumers

---

## Strategy 5: Event Schema Registry (for event-driven systems)

**When to use:** Asynchronous event schemas need to evolve across decoupled producers and consumers.

**How it works:**
- All schemas are registered in a schema registry (Confluent Schema Registry, AWS Glue, etc.)
- Compatibility modes enforce rules: `BACKWARD` (new schema can read old data),
  `FORWARD` (old schema can read new data), `FULL` (both)
- Producers and consumers negotiate schema version at runtime

**Best for:** Kafka, SQS, EventBridge, or any event streaming system
**Tradeoffs:** Requires schema registry infrastructure; adds operational complexity

---

## Migration window guidelines

| Consumer type | Suggested minimum window | Notes |
|--------------|--------------------------|-------|
| Internal services (same org) | 2–4 weeks | Coordinate directly; can track adoption |
| Mobile apps (iOS/Android) | 3–6 months | App store review + user update lag |
| Partner integrations | 90 days minimum | Often contractual; may need SLA notice |
| Public API with unknown consumers | 6–12 months | Can't contact everyone; monitor traffic |
| Generated SDK clients | Until new SDK published + adopted | Track SDK version in API logs |

---

## Deprecation signals

Use these in API responses to communicate upcoming removals:

**HTTP headers (REST):**
```
Deprecation: true
Sunset: Sat, 01 Jun 2025 00:00:00 GMT
Link: <https://docs.example.com/migration>; rel="deprecation"
```

**OpenAPI:**
```yaml
properties:
  legacy_id:
    type: integer
    deprecated: true
    description: "Deprecated. Use `id` instead. Will be removed 2025-06-01."
```

**GraphQL:**
```graphql
type Payment {
  legacyId: Int @deprecated(reason: "Use `id`. Will be removed 2025-06-01.")
  id: String!
}
```

---

## The "dark launch" check

Before removing any field or endpoint, verify no consumers are still using it:

```bash
# Check access logs for old endpoint traffic
grep "GET /api/v1/payments" access.log | wc -l

# Check for old field name in consumer code
grep -rn "legacy_id\|amount\"" services/ --include="*.py" --include="*.js"

# For REST APIs with detailed logging, check field access patterns
# (requires structured logging that captures which response fields were accessed)
```

Zero traffic / zero references ≠ safe to remove — there may be infrequent consumers,
batch jobs, or cached clients. But it's a strong signal.