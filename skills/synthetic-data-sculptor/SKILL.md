---
name: synthetic-data-sculptor
description: >
  Generates high-quality synthetic test data — JSON, CSV, SQL — without touching production
  databases. Use this skill whenever the user needs: fake but realistic test data, edge case data
  (boundary values, special characters, extreme lengths), data for specific demographics or
  scenarios (e.g., "elderly users with expired cards"), stress-test data (huge strings, RTL text,
  far-future dates), safe anonymized stand-ins for production data, or factory-based fixture
  generation. Trigger for phrases like "generate test data", "fake data", "seed the database",
  "create sample users", "test fixtures", "mock data", "stress data", "edge case data",
  "generate N records", "Faker data", "seed file", "fixture file", "data generator", "factory
  data", or any request to produce structured data for testing purposes.
---

# Synthetic Data Sculptor

Generates safe, realistic, and edge-case-rich test data without touching production. You create data that's both plausible (won't break domain validations) and strategically weird (will find bugs).

## Workflow

### Step 1: Understand the schema

Ask for (or derive from context):
- **Entity types** needed (Users, Orders, Products, etc.)
- **Field names and types** for each entity
- **Constraints** (max lengths, required fields, valid ranges, foreign key relationships)
- **Format** desired (JSON, CSV, SQL INSERT statements)
- **Count** of records needed

If the user provides a SQL schema, database migration file, or API spec, parse it directly to extract field metadata.

### Step 2: Choose a generation strategy

| Scenario | Strategy |
|----------|----------|
| Standard realistic data | Use `scripts/generate_data.py` with Faker |
| Specific demographics / scenarios | Use LLM-guided generation with `scripts/generate_data.py --scenario` |
| Edge cases / stress data | Use `references/edge-case-catalog.md` as input spec |
| SQL INSERT format | Add `--format sql` flag and provide table name |
| Relational data (FK constraints) | Generate parents first, use their IDs for child records |

### Step 3: Generate the data

**Standard generation:**
```bash
python scripts/generate_data.py \
  --schema references/schema_templates/users.json \
  --count 100 \
  --format json \
  --output /tmp/test-data/users.json
```

**Scenario-based generation** (uses LLM guidance internally):
```bash
python scripts/generate_data.py \
  --schema references/schema_templates/users.json \
  --scenario "users over 65 with expired credit cards in the US" \
  --count 50 \
  --output /tmp/test-data/elderly_users.json
```

**Edge case / stress data:**
```bash
python scripts/generate_data.py \
  --schema references/schema_templates/users.json \
  --edge-cases \
  --output /tmp/test-data/edge_users.json
```

### Step 4: Validate the output

Before delivering data to the user:
1. Check that required fields are always populated
2. Verify that foreign key values actually exist in parent records
3. Spot-check a few records for realism — names should look like names, emails like emails
4. Confirm counts match what was requested

### Step 5: Deliver

Provide the generated file(s) and a brief summary:
- How many records generated
- What edge cases are included (if any)
- How to use the data (e.g., SQL import command, how to load JSON fixtures)

## Edge case thinking

When generating edge cases, always think about:

**Strings**: Empty string `""`, single character, 255 chars (common DB limit), 256 chars (one over), 1000 chars, emoji (`🚀💯`), HTML tags (`<script>alert(1)</script>`), null byte (`\0`), SQL injection attempts (`'; DROP TABLE users; --`), RTL text (`مرحبا بالعالم`), unicode normalization edge cases

**Numbers**: 0, -1, max int, min int, float precision edge cases (0.1 + 0.2), very large numbers

**Dates**: Epoch (1970-01-01), far past (1900-01-01), far future (2099-12-31), leap day (2000-02-29), timezone edge cases, daylight saving transition days

**Emails / usernames**: Unicode domains (`user@münchen.de`), subaddressing (`user+tag@example.com`), max-length (254 chars), case variations

**Addresses**: RTL countries, very long street names, PO Boxes, missing postal codes, non-standard formats

## Schema templates

Pre-built schemas in `references/schema_templates/`:
- `users.json` — User accounts (name, email, DOB, address, phone)
- `orders.json` — E-commerce orders (items, amounts, status, timestamps)
- `products.json` — Product catalog (name, SKU, price, inventory)
- `payments.json` — Payment records (card data stub, amounts, currency)

## Reference files

- `references/edge-case-catalog.md` — Comprehensive edge case values by data type
- `references/schema_templates/` — Pre-built entity schemas
- `scripts/generate_data.py` — Main data generation script (Faker-based)