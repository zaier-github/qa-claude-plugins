# Test Strategy Template

Use this template when writing `test-strategy.md`.

---

```markdown
# Test Strategy: {Release / Feature Set Name}

**Version**: 1.0  
**Date**: {YYYY-MM-DD}  
**Scope**: {N} requirements, {M} components  
**Risk Level**: High / Medium / Low  
**Prepared by**: QA Team

---

## 1. Testing Objectives and Scope

### Objectives
1. Validate all {N} acceptance criteria across {N} requirements
2. Ensure integration between {Component A} and {Component B} functions correctly
3. Verify security controls for {authentication / authorization / data access}
4. Achieve {X}% regression automation coverage

### Scope

**In scope**:
- Requirements: {KEY-1}, {KEY-2}, ...
- Components: {list}
- User workflows: {list}
- Integration points: {list}
- Platforms: {browsers, OS, devices}

**Out of scope**:
- {Excluded area + rationale}

### Context
| Attribute | Value |
|---|---|
| Release type | Major / Minor / Patch |
| Business impact | High / Medium / Low |
| Target users | {User personas} |
| Key dependencies | {External systems} |

---

## 2. Test Levels

### 2.1 Integration Testing
**Objective**: Validate component interactions, API contracts, and data flows between services.

**Approach**:
- API endpoint contract testing
- Database integration validation
- External system integration (with stubs/mocks where unavailable)
- Event/message queue testing (if applicable)

**Coverage target**: All {N} integration points identified in requirements.

**Entry criteria**: Unit tests passing; components independently deployable.  
**Exit criteria**: All integration scenarios pass; no Critical or High defects open.

### 2.2 System Testing
**Objective**: Validate complete end-to-end behavior against business requirements.

**Approach**:
- End-to-end user workflow execution
- Business rule verification against acceptance criteria
- Cross-browser / cross-platform testing (list targets)
- Data flow validation

**Coverage target**: 100% of functional requirements; 100% of acceptance criteria.

**Entry criteria**: Integration testing complete; stable system environment.  
**Exit criteria**: All system tests pass; requirements sign-off from QA.

### 2.3 User Acceptance Testing (UAT)
**Objective**: Confirm system meets business expectations and user needs.

**Approach**:
- Business scenario walkthroughs with key stakeholders
- User workflow validation by representative users
- Usability assessment (informal)

**Coverage target**: All critical business workflows; formal AC sign-off.

**Entry criteria**: System testing complete; business stakeholders available.  
**Exit criteria**: UAT sign-off; accepted defects documented.

---

## 3. Test Types

### 3.1 Functional Testing _(always included)_
Covers all acceptance criteria. Primary test type.

### 3.2 Security Testing _(include if requirements contain auth/PII/compliance)_
- Authentication and session management
- Role-based access control verification
- Input sanitization and injection prevention
- Sensitive data exposure checks

### 3.3 Performance Testing _(include if NFRs specify targets)_
- Load testing: {N} concurrent users, {X}s response time target
- Stress testing: identify degradation point
- Tools: k6 / JMeter / Locust

### 3.4 Regression Testing _(always included)_
- Scope: {X} existing test cases in regression suite
- Frequency: full suite per release; smoke suite per deployment
- Automation target: {60–70}% of regression suite

---

## 4. Test Design Techniques

| Technique | Applied to |
|---|---|
| Equivalence Partitioning | Input field validation, data classification |
| Boundary Value Analysis | Numeric fields, date ranges, string lengths |
| Decision Table Testing | Complex conditional business rules |
| State Transition Testing | Workflow statuses, approval flows |
| Use Case Testing | Multi-step user journeys |
| Error Guessing | Known defect-prone areas, error handling |

---

## 5. Automation Approach

**Framework**: Playwright (TypeScript) with Page Object Model pattern.

**What to automate**: regression suite, API integration tests, data-driven scenarios, smoke suite.

**What NOT to automate**: exploratory testing, one-time scenarios, usability, tests requiring human judgment.

**Structure**:
- `tests/e2e/` — Playwright end-to-end tests
- `tests/api/` — API integration tests
- `pages/` — Page Object Models
- `fixtures/` — Test data and configuration

**CI integration**: Smoke suite on every PR merge; full regression nightly.

**Coverage target**: {60–70}% of regression test suite automated by release.

---

## 6. Quality Metrics

| Metric | Target |
|---|---|
| Requirements coverage | 100% |
| AC coverage | 100% |
| Test execution rate | ≥ 95% |
| Defect density | ≤ 0.25 defects/requirement |
| P1/P2 open at exit | 0 |
| Automation coverage | ≥ 60% |
| Flakiness rate | ≤ 5% |

---

## 7. Risk-Based Testing Priority

| Risk Score | Coverage Level | Automation Priority |
|---|---|---|
| 15–25 (Critical/High) | Comprehensive — all test types | Highest |
| 8–14 (Medium) | Standard — functional + regression | Medium |
| 1–7 (Low) | Smoke-level validation | Low |

High-risk requirements (see risk register): {KEY-1}, {KEY-2}

---

_Generated by generate-test-strategy on {date}_
```
