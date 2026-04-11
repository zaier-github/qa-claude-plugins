# Schema Format Analysis: GraphQL, Protobuf, AsyncAPI, JSON

Analysis guidance for non-OpenAPI schema formats.

---

## GraphQL Schema Analysis

### What to diff
GraphQL schemas define types, queries, mutations, and subscriptions. The SDL (Schema Definition Language) is the canonical form.

**Breaking changes in GraphQL:**
- Field removed from any type → 🔴 breaking (clients querying that field get an error)
- Field type changed (non-null ↔ nullable, String ↔ Int) → 🔴 breaking
- Required argument added to field/query/mutation → 🔴 breaking
- Argument removed or renamed → 🔴 breaking if clients send it (error or silently ignored)
- Type removed from schema → 🔴 breaking
- Enum value removed → 🔴 breaking
- Interface or union type changed (member removed) → 🔴 breaking
- Query/Mutation/Subscription operation removed → 🔴 breaking

**Non-breaking in GraphQL:**
- New type added → 🟢
- New field added to type → 🟢 (clients not querying it are unaffected)
- Required field made nullable → 🟢 (clients that didn't null-check may be surprised, but no error)
- New enum value added → ⚠️ hidden risk (exhaustive switch in client code)
- New optional argument added → 🟢
- `@deprecated` directive added → 🟡 soft warning

**GraphQL-specific risk: nullable → non-null (!):**
A field changing from nullable to required (`String` → `String!`) is *technically*
non-breaking per the schema, but if clients were handling null and the server was
sometimes returning null, making it required at the schema level while keeping the
server logic may expose previously-masked null returns as errors.

**Tooling:**
```bash
# graphql-inspector
npx @graphql-inspector/cli diff old-schema.graphql new-schema.graphql

# graphql-schema-diff
npx graphql-schema-diff old-schema.graphql new-schema.graphql
```

---

## Protobuf / gRPC Analysis

Protobuf has formal field numbering that determines wire compatibility. The key rule:
**field numbers are permanent** — changing a field number is always breaking at the
wire level even if the field name stays the same.

### Breaking changes in Protobuf
- Field number reused for different type → 🔴 breaking (wire corruption)
- Field removed without being marked `reserved` → 🔴 breaking (number can be reused,
  old clients sending the field will have it silently ignored OR misinterpreted)
- Required field added (proto2 only) → 🔴 breaking
- Field type changed → 🔴 breaking (usually; some type changes are wire-compatible)
- RPC method removed → 🔴 breaking
- Service removed → 🔴 breaking
- Enum first value (0) changed → 🔴 breaking (proto3 defaults to 0 for unknown values)

### Safe in Protobuf
- New optional field added with unused number → 🟢 (old clients ignore it, new clients get it)
- New enum value added (non-zero) → 🟢 (old clients get UNRECOGNIZED)
- New RPC method added → 🟢
- Field name changed (NOT number) → 🟢 for binary serialization, 🔴 for JSON serialization

### The `reserved` keyword
When removing a field, always mark the field number as `reserved`:
```proto
message Payment {
  reserved 3;  // was: string legacy_id = 3;
  reserved "legacy_id";
  int64 id = 1;
  double amount = 2;
}
```
Without `reserved`, the field number can be accidentally reused by a future field,
causing silent wire-level data corruption in old clients.

**Tooling:**
```bash
# buf breaking (highly recommended)
buf breaking --against .git#branch=main
# or
buf breaking --against old-proto-dir/
```

---

## AsyncAPI / Event Schema Analysis

Event-driven systems have higher stakes than REST because producer and consumer deploys
are decoupled. A breaking event schema change can silently corrupt message processing
for hours before anyone notices.

### What to diff
AsyncAPI specs define channels (topics/queues) and message schemas:

```yaml
asyncapi: "2.6.0"
channels:
  payment/completed:
    publish:
      message:
        payload:
          type: object
          required: [payment_id, amount, user_id]
          properties:
            payment_id: { type: string }
            amount: { type: number }
            user_id: { type: string }
            currency: { type: string, default: "USD" }
```

### Breaking changes in events
- Required field removed from payload → 🔴 breaking (consumers get null/deserialization error)
- Field type changed → 🔴 breaking
- Field renamed → 🔴 breaking (functionally a removal)
- Channel/topic renamed → 🔴 breaking (consumers subscribed to old name stop receiving)
- Event type discriminator changed → 🔴 breaking
- Message envelope format changed → 🔴 breaking

### The dead letter queue test
A useful mental model: if this change ships and old consumers keep running, will they
start producing dead-letter messages? If yes → 🔴 breaking. If they'll process messages
but with wrong data → 🟠 silently breaking.

### Event versioning patterns
Unlike REST, you can't version-negotiate per-request with events. Options:
- **Additive only**: Never remove or change fields; only add optional new ones
- **Message versioning**: Add a `schema_version` field and run parallel consumers
- **New event type**: `payment.completed.v2` alongside `payment.completed`
- **Consumer-side schema evolution**: Avro/Protobuf schemas with registry

---

## Plain JSON / TypeScript Shape Analysis

When working with plain JSON shapes, TypeScript interfaces, Zod schemas, or other
non-formal contracts, the analysis is the same — just the source format differs.

### TypeScript interfaces
```typescript
// Old
interface PaymentResponse {
  id: string;
  amount: number;        // was always present
  legacyId?: number;     // optional
  status: 'pending' | 'complete' | 'failed';
}

// New
interface PaymentResponse {
  id: string;
  totalAmount: number;   // renamed from amount — BREAKING
  // legacyId removed    — BREAKING if any consumer used it
  status: 'pending' | 'complete' | 'failed' | 'review';  // new enum — hidden risk
  currency: string;      // new required field — non-breaking for response
}
```

### Zod schemas
Zod schemas are executable TypeScript — if both old and new schemas are available,
they can be run against sample payloads to detect compatibility:
```typescript
const oldSchema = z.object({ amount: z.number() });
const newResponse = { totalAmount: 99.99 }; // amount missing
oldSchema.parse(newResponse); // throws ZodError — confirms breaking change
```

### JSON Schema
Follow OpenAPI analysis rules — JSON Schema is the underlying format OpenAPI uses
for its schemas. Key keywords: `required`, `properties`, `type`, `enum`, `additionalProperties`.