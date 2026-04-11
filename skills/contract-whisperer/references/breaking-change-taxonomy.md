# Breaking Change Taxonomy

Classification rules for every type of contract change. The key question for each change:
*can an existing consumer, written against the old contract and not yet updated, continue to
work correctly?* If no → breaking. If maybe → potentially breaking. If yes → non-breaking.

---

## Table of Contents
1. [Response Shape Changes](#1-response-shape-changes)
2. [Request Contract Changes](#2-request-contract-changes)
3. [Type and Format Changes](#3-type-and-format-changes)
4. [Behavioral Contract Changes](#4-behavioral-contract-changes)
5. [Authentication and Authorization Changes](#5-authentication-and-authorization-changes)
6. [Endpoint / Operation Changes](#6-endpoint--operation-changes)
7. [Error Response Changes](#7-error-response-changes)
8. [Event / Message Schema Changes](#8-event--message-schema-changes)
9. [Additive Changes with Hidden Risks](#9-additive-changes-with-hidden-risks)

---

## 1. Response Shape Changes

### 🔴 Breaking
- **Field removed**: Any field present in the old response is absent in the new one.
  Consumers reading that field get `null`, `undefined`, `KeyError`, or a deserialization error.
- **Field renamed**: Functionally a removal + addition. The old name is gone; consumers
  using the old name break even though the data still exists under a new name.
- **Nested object flattened or deepened**: `response.user.address.city` → `response.city`
  or the reverse. Path-based consumers break.
- **Array replaced with object** (or vice versa): Consumers iterating an array that's now
  an object will get a type error; consumers accessing a key on what's now an array will fail.
- **Nullable field made non-nullable**: Consumers that handle the null case are now handling
  a case that can't occur — not strictly breaking, but tests expecting null will fail.

### 🟠 Potentially Breaking
- **Field semantics changed without type change**: `status` still returns a string but the
  possible values have changed meaning. Type-safe consumers are fine; logic-dependent consumers break.
- **Response structure reorganized**: Data moved between nesting levels or sibling keys.
  Looser consumers (reading only what they need) may be fine; strict consumers break.
- **Previously guaranteed field made optional**: Consumers that don't null-check will eventually
  encounter a null and fail. May not break immediately but will in production.

### 🟢 Non-Breaking
- **New optional field added**: Consumers that don't know about it will ignore it.
  *Exception*: strict deserializers set to reject unknown fields will break — flag this.
- **Previously optional field made required** (in response, not request): Consumers
  expecting null will now always get a value — generally safe, but null-handling code
  may behave differently.

---

## 2. Request Contract Changes

### 🔴 Breaking
- **New required field added**: Existing requests without this field will be rejected (400/422).
- **Required field removed from the schema** (but still validated server-side): Requests
  that don't send it will now fail validation that wasn't in the spec.
- **Valid enum value removed from request**: Requests sending the old value will be rejected.
- **Request body format changed**: JSON → form-data, or content-type requirements changed.

### 🟠 Potentially Breaking
- **Default value for optional field changed**: Consumers not sending the field will now
  get different behavior without changing their code.
- **Validation rules tightened**: A field that accepted any string now requires a specific
  format. Old consumers sending previously-valid values will start getting errors.
- **Query parameter renamed or repurposed**: Old parameter silently ignored; new behavior
  diverges from what consumer expects.

### 🟢 Non-Breaking
- **New optional field added to request**: Consumers not sending it continue to work.
- **Required field made optional**: Consumers that always sent it are unaffected.
- **Validation rules loosened**: Previously-rejected values now accepted.

---

## 3. Type and Format Changes

### 🔴 Breaking (almost always)
- **String → Integer** (or any numeric type): JSON consumers may handle this with implicit
  coercion; strictly-typed languages (Swift, Kotlin, Go, Rust) will throw a deserialization error.
- **Integer → String**: Same issue in reverse.
- **String → Boolean**: High break risk.
- **Object → Array** or vice versa: Always breaking.
- **Date format change**: `"2024-01-15"` → `1705276800` (Unix timestamp). Parsers will fail
  or produce wrong values.
- **Precision change** (float → int): Data loss. Monetary values especially dangerous.
- **String format change**: `uuid` → `nanoid`, or ISO date → custom format.

### 🟠 Potentially Breaking
- **Null added to type** (field can now be null that wasn't before): Strictly-typed
  consumers that don't handle null will crash when null is eventually returned.
- **Integer width change**: `int32` → `int64` may overflow in some client languages.
- **Number precision increased**: Generally safe, but exact-comparison code will break.

---

## 4. Behavioral Contract Changes

These are the hardest to detect because the schema doesn't change — only the behavior does.

### 🔴 Breaking
- **Idempotency removed**: Endpoint was safe to retry; now it isn't. Consumers with retry
  logic will cause duplicate operations (double charges, duplicate records).
- **Synchronous → Asynchronous**: Endpoint used to return the result; now returns a job ID.
  Consumers expecting the result immediately will get wrong data.
- **Pagination behavior changed**: Cursor-based → offset-based, or page size limits changed.
  Consumers with pagination logic will miss data or duplicate-fetch.
- **Ordering guarantees removed**: Results were implicitly ordered; now they aren't.
  Consumers relying on order will get non-deterministic behavior.

### 🟠 Potentially Breaking
- **Caching headers changed**: More aggressive caching may serve stale data to consumers
  that expected fresh results.
- **Rate limit thresholds changed**: Consumers calibrated to old limits will start
  getting 429s.
- **Semantics of an existing status code changed**: `404` now means something different
  from what consumers expect.

---

## 5. Authentication and Authorization Changes

### 🔴 Breaking
- **Authentication required where it wasn't**: Unauthenticated consumers will get 401.
- **Scope requirement added**: OAuth consumers without the new scope will get 403.
- **API key format changed**: Old keys rejected.
- **Token expiry shortened**: Consumers with long-lived tokens will start seeing auth errors
  sooner than expected.

### 🟠 Potentially Breaking
- **New optional auth scheme**: Consumers using old scheme continue to work but may not
  benefit from improved security.
- **JWT claim structure changed**: Consumers parsing JWT payloads directly will get wrong data.

---

## 6. Endpoint / Operation Changes

### 🔴 Breaking
- **Path changed**: `/api/v1/users/{id}` → `/api/v1/accounts/{id}`. All consumers get 404.
- **HTTP method changed**: `POST` → `PUT` for an operation. Consumers using old method get 405.
- **Endpoint removed**: All consumers get 404 or 410.
- **Host or base URL changed**: All consumers fail to connect.

### 🟠 Potentially Breaking
- **Endpoint deprecated but not removed**: Consumers will continue to work but should migrate.
  Flag if no deprecation header (`Deprecation`, `Sunset`) is present.

### 🟢 Non-Breaking
- **New endpoint added**: Existing consumers unaffected.
- **Old endpoint aliased to new path**: Both work; consumers on old path continue to work.

---

## 7. Error Response Changes

### 🟠 Potentially Breaking (often overlooked)
- **Error response shape changed**: Consumers parsing error bodies to extract messages or
  codes will get wrong data or parse failures.
- **HTTP status codes changed**: `400` → `422` for validation errors. Consumers branching
  on status codes will hit the wrong branch.
- **New error codes added**: Consumers with exhaustive error handling will hit an unhandled case.
- **Error field renamed**: `error.message` → `error.detail`. Consumers reading the old field
  get undefined/null.

---

## 8. Event / Message Schema Changes

Events are higher-risk than REST API changes because consumers are decoupled — you can't
coordinate their deployment with the producer's deployment.

### 🔴 Breaking
- **Required event field removed**: Consumers reading it get null or deserialization failure.
- **Event type renamed**: Consumers subscribed to old event type stop receiving events.
- **Message format changed** (JSON → Avro, etc.): Complete consumer failure.
- **Topic/queue renamed or removed**: Consumer subscriptions silently stop working.

### 🟠 Potentially Breaking
- **Event field renamed**: Functionally a removal — consumers on old name get no data.
- **New required field added to event**: Producers that don't send it will fail; consumers
  expecting it will get null from old producers during transition.
- **Event semantics changed**: Same event type now means something different. Consumers
  taking action on it will take the wrong action.

### 🟢 Non-Breaking
- **New optional field added**: Consumers that don't use it are unaffected.
- **New event type added**: Consumers not subscribed to it are unaffected.

---

## 9. Additive Changes with Hidden Risks

These are classified non-breaking but warrant a callout because they bite consumers anyway:

- **New enum value**: Non-breaking per spec, but consumers using exhaustive switch/match/when
  statements (Swift `switch`, Rust `match`, TypeScript exhaustive checks) will get a compile
  error or runtime panic. Always flag new enum values.
- **Strict deserializer consumers**: Some frameworks reject unknown fields by default
  (Jackson with `FAIL_ON_UNKNOWN_PROPERTIES`, .NET with `MissingMemberHandling.Error`).
  New fields in a response will break these consumers even though the change is "additive."
- **Generated clients**: SDK clients generated from the old spec won't know about new fields
  until regenerated. The change is safe at the protocol level but requires a client update.
- **OpenAPI `additionalProperties: false`**: If the old spec declared `additionalProperties: false`,
  consumers using spec-generated validators will reject responses with new fields.