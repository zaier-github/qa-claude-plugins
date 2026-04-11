# Test Case Priority Guide

## Priority definitions

### P1 — Critical
**When**: The tested scenario protects against catastrophic or irreversible outcomes.

Applies to:
- Authentication and authorization flows
- Payment processing and financial calculations
- Personal data protection (PII/GDPR compliance)
- Data integrity and loss prevention
- Security controls (access, encryption, audit trails)
- Regulatory or compliance requirements
- System stability under expected load

**Rule**: If this test fails and reaches production, the impact is severe and immediate.

### P2 — High
**When**: Core business functionality — failure significantly degrades user experience or business value.

Applies to:
- Primary happy-path workflows for main features
- Core CRUD operations (create, read, update, delete)
- Key integrations with other systems
- Business rule enforcement (discounts, eligibility, routing)
- Email/notification delivery for business processes

**Rule**: Most features generate mostly P2 tests. P2 is the default for acceptance-criteria-driven tests.

### P3 — Medium
**When**: Standard feature behavior — failure is annoying but users can work around it.

Applies to:
- Input validation and form field rules
- UI state and display accuracy
- Non-critical workflow variations
- Sorting, filtering, pagination
- Error messages and user-facing copy
- Secondary/optional features

**Rule**: P3 tests are important but can be deferred from a blocking release gate in some cases.

### P4 — Low
**When**: Cosmetic, low-frequency edge cases, or scenarios with minimal business impact.

Applies to:
- Purely cosmetic UI issues (alignment, spacing)
- Very rare edge cases (extreme inputs, unusual character sequences)
- Optional feature enhancements
- Nice-to-have behaviors not in acceptance criteria

**Rule**: P4 tests should be run but rarely block releases. Use sparingly — only one or two per requirement maximum.

## Common mistakes

| Mistake                             | Correct approach                                                     |
|-------------------------------------|----------------------------------------------------------------------|
| Assigning P1 to all test cases      | P1 is reserved for security/integrity/compliance — most tests are P2 |
| Assigning P3 to login flows         | Login is P1 (authentication = critical)                              |
| Assigning P1 to every negative test | Negative tests are usually P2 or P3 unless they test security bypass |
| No P4 tests at all                  | P4 is valid for cosmetic checks — just don't over-assign             |
