# OpenAPI / Swagger Analysis

How to diff and analyze OpenAPI 3.x and Swagger 2.x specifications for breaking changes.

---

## Parsing the spec

OpenAPI specs are YAML or JSON. Key structural sections:

```yaml
openapi: "3.0.3"
info:
  title: Payments API
  version: "2.1.0"
paths:
  /payments/{id}:
    get:
      operationId: getPayment
      parameters: [...]
      requestBody: {...}
      responses:
        "200":
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Payment"
components:
  schemas:
    Payment:
      type: object
      required: [id, amount, status]
      properties:
        id: { type: string }
        amount: { type: number }
        status: { type: string, enum: [pending, complete, failed] }
        legacy_id: { type: integer, deprecated: true }
```

---

## What to diff

### Paths (endpoints)
- Added paths → non-breaking
- Removed paths → 🔴 breaking
- Changed HTTP methods for existing operations → 🔴 breaking
- Changed path parameters → 🔴 breaking (changes the URL structure)
- `deprecated: true` added → 🟡 soft break (warning, not yet removed)

### Parameters
- Required parameter added → 🔴 breaking (consumers not sending it get 400/422)
- Required parameter removed → 🟢 non-breaking (consumers still sending it usually OK)
- Optional parameter removed → 🟠 potentially breaking (if consumers depend on it)
- Parameter type changed → 🔴 breaking
- Parameter validation tightened → 🟠 potentially breaking

### Request bodies
- New required field → 🔴 breaking
- Required field made optional → 🟢 non-breaking
- Optional field removed → 🟠 potentially breaking
- Type change on any field → 🔴 breaking

### Response schemas
Walk `responses > "200" > content > application/json > schema` (and all $ref resolutions).
For each property in the old schema:
- Still present with same type? → non-breaking
- Present but type changed? → 🔴 breaking
- Absent in new schema? → 🔴 breaking (field removed)
- Was required, now optional? → 🟠 potentially breaking
- Was optional, now required? → 🟢 non-breaking (for responses)

For new properties in the new schema:
- Added as optional? → 🟢 non-breaking (with caveats for strict deserializers)
- Added as required? → 🟢 non-breaking (for responses — consumers get more data)
- New enum value? → ⚠️ hidden risk

### $ref resolution
Trace all `$ref` references in both specs. A change to a shared component schema propagates
to every endpoint that uses it. Always resolve refs before diffing.

```python
# Resolve $ref references in Python
import yaml, json
from jsonref import replace_refs

with open('openapi_new.yaml') as f:
    spec = yaml.safe_load(f)
resolved = replace_refs(spec)
# Now traverse resolved rather than spec
```

### Security schemes
- New security requirement added to existing operation → 🔴 breaking
- Security requirement removed → 🟢 non-breaking (but may be a security regression)
- OAuth scope added → 🔴 breaking for consumers without the new scope

---

## Command-line tools (if available)

```bash
# openapi-diff (Java-based, very thorough)
openapi-diff old-spec.yaml new-spec.yaml --fail-on-incompatible

# oasdiff (Go-based, fast)
oasdiff breaking old-spec.yaml new-spec.yaml

# speccy lint (basic validation)
speccy lint new-spec.yaml

# swagger-diff
swagger-diff old-spec.json new-spec.json
```

---

## Swagger 2.x differences

Swagger 2.x uses `swagger: "2.0"` and has slightly different structure:
- `definitions` instead of `components/schemas`
- `parameters` with `in: body` for request bodies (no `requestBody`)
- `produces`/`consumes` arrays at spec or operation level
- Response schemas directly under `responses > "200" > schema`

The breaking change rules are the same; only the path to find them differs.

---

## High-risk patterns to flag

- **`additionalProperties: false`** on any response schema: New fields added elsewhere
  in the response will cause validation failures for consumers using spec validators.
- **`allOf` composition changed**: Removing a member of `allOf` removes all its fields
  from the effective schema — high-impact breakage that's easy to miss.
- **Polymorphic schemas (`oneOf`, `anyOf`) with discriminator changed**: The discriminator
  field name or value mapping change is always breaking.
- **`nullable: true` removed**: Field that was nullable is no longer — may break consumers
  that explicitly handle null.
- **Format constraints added** (`format: email`, `format: uuid`): Previously-valid values
  that don't match the new format will now fail validation.