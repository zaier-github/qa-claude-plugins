# Quality Scoring Guide

## Completeness Score

Measures whether the required fields are populated.

**Required fields (each worth equal weight)**:
- Summary (always present if the ticket exists)
- Description (body of the ticket)
- Acceptance Criteria (custom field OR parsed from description)
- Assignee
- Components
- Fix Version / Sprint

**Score**: `(fields present / 6) × 100`

| Range   | Level  | Meaning                                                      |
|---------|--------|--------------------------------------------------------------|
| 80–100% | High   | All key fields present; ready for test generation            |
| 50–79%  | Medium | Missing some fields; test generation possible but incomplete |
| < 50%   | Low    | Missing critical fields; flagged for requirement owner       |

## Quality Score

Measures the *usefulness* of the content present.

**Criteria (each 0–20 points)**:

| Criterion                       | 0 pts                                         | 10 pts                          | 20 pts                                                        |
|---------------------------------|-----------------------------------------------|---------------------------------|---------------------------------------------------------------|
| **Clarity**                     | Vague or missing description                  | Partially clear, some ambiguity | Unambiguous, specific, no jargon without definition           |
| **AC Specificity**              | No AC / generic statements ("it should work") | Some specific criteria          | All criteria testable and measurable                          |
| **Examples**                    | No examples                                   | Some implicit context           | Concrete examples or test data given                          |
| **Scope Definition**            | No in/out scope                               | Partially defined               | Clearly states what IS and IS NOT included                    |
| **Non-functional Requirements** | No NFRs mentioned                             | NFRs implied                    | Explicit performance, security, or accessibility requirements |

**Quality levels**:

| Range  | Level     |
|--------|-----------|
| 90–100 | Excellent |
| 70–89  | Good      |
| 50–69  | Fair      |
| < 50   | Poor      |

## Recommendation generation rules

| Condition                              | Recommendation                                                                               |
|----------------------------------------|----------------------------------------------------------------------------------------------|
| No acceptance criteria                 | "Add explicit, testable acceptance criteria — this is required for test generation"          |
| AC exists but vague ("it should work") | "Rewrite acceptance criteria as Given/When/Then or specific measurable outcomes"             |
| Missing description                    | "Add a description explaining business context and user value"                               |
| Missing fix version                    | "Assign a fix version to enable release-scoped analysis"                                     |
| Missing components                     | "Assign components to enable component-based risk analysis"                                  |
| Quality score < 50                     | "This requirement needs significant improvement before test cases can be reliably generated" |
