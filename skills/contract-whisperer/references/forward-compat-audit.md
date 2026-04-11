# Forward Compatibility Audit

How to audit a *single* spec version for patterns that will cause pain when the API
evolves in the future — before any breaking change has been made.

---

## When to use this

The user provides one spec with no "before" version, and wants to know:
- "Is this API designed to be evolvable?"
- "What patterns here will make future changes painful?"
- "What should we fix now before consumers depend on it?"

---

## Anti-patterns to flag

### 1. No versioning strategy
No version in the path, no version header, no version negotiation. When the first
breaking change is needed, there's no safe way to ship it.

**Flag:** Recommend adding a version prefix (`/v1/`) or header strategy now, before
consumers build against the unversioned API.

### 2. Over-specified response contracts
- `additionalProperties: false` on response schemas: Prevents adding new fields without
  breaking spec-validating consumers.
- Extremely tight `maxLength`, `pattern`, or `format` constraints on fields that may
  need to evolve (e.g., `maxLength: 10` on an ID field).

**Flag:** Recommend removing `additionalProperties: false` from response schemas (it's
appropriate for request validation, not response definition).

### 3. Enum sprawl without extensibility hints
Enums in responses that will inevitably grow (order status, event types, payment methods)
with no hint that new values may be added.

**Flag:** Add a comment/description noting that new values may be added. Advise consumers
to handle unknown enum values gracefully.

### 4. Required fields in responses with uncertain futures
Marking fields `required` in responses that might reasonably become optional or be
removed in future versions (e.g., a field tied to a feature that could be deprecated).

**Flag:** Discuss whether these fields are truly permanent or might change.

### 5. Tightly coupled field names
Fields named after internal concepts, implementation details, or vendor-specific systems
(e.g., `stripe_charge_id`, `postgres_row_id`). These become painful to rename when the
implementation changes.

**Flag:** Recommend abstracted field names that describe intent, not implementation.

### 6. No deprecation mechanism
The spec has no `deprecated` markers, no sunset date convention, and no documentation
of how deprecated fields will be communicated.

**Flag:** Recommend establishing a deprecation policy before the first deprecation is needed.

### 7. Polymorphism without discriminator
`oneOf` or `anyOf` schemas without a `discriminator` field make it hard for clients to
parse responses correctly and even harder to extend the schema later.

**Flag:** Add a discriminator field to all polymorphic response types.

### 8. Inconsistent nullability
Some fields are `nullable: true`, some are not, with no apparent pattern. When consumers
learn which fields can be null from experience rather than the spec, removing null from
a field that was sometimes null in practice is a surprise breaking change.

**Flag:** Audit all fields for intentional nullability and document it consistently.

---

## Evolvability score

After the audit, assign an overall evolvability score:

| Score | Meaning |
|-------|---------|
| ✅ High | Versioned, extensible, no major anti-patterns. Future changes will be manageable. |
| ⚠️ Medium | Some anti-patterns present. Future evolution will require careful coordination. |
| ❌ Low | Multiple anti-patterns. The first significant API change will likely break consumers. |