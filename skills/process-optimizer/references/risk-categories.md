# Risk Categories and Detection Guide

## Risk identification approach

Risks are identified by scanning the epic description, child story summaries, and descriptions for keyword patterns. Each detection triggers a risk entry with default scores that the analyst should review and adjust.

---

## Risk scoring

```
risk_score = impact_score × probability_score

Impact:      Critical=5, High=4, Medium=3, Low=2, Negligible=1
Probability: Very High=5, High=4, Medium=3, Low=2, Very Low=1

Priority:
  Critical: score ≥ 20
  High:     score 15–19
  Medium:   score 9–14
  Low:      score < 9
```

---

## Risk catalog

### RISK-001: Integration Complexity
**Keywords**: API, integration, third-party, external, service, microservice, webhook, REST, GraphQL  
**Default**: Impact=High(4), Probability=High(4), Score=16, Priority=High  
**Owner**: Tech Lead / Integration Team  
**Mitigations**:
- Set up mock services for independent testing
- Define clear API contracts and validate with consumer-driven tests
- Implement integration tests with TestContainers or similar
- Plan for third-party service downtime scenarios (stubs, circuit breakers)

---

### RISK-002: Data Complexity
**Keywords**: migration, database, schema, data model, legacy data, ETL, transform  
**Default**: Impact=High(4), Probability=Medium(3), Score=12, Priority=Medium  
**Owner**: Data Team / QA Lead  
**Mitigations**:
- Create comprehensive test data sets covering edge cases
- Test migration scripts in isolated environment before prod
- Implement rollback procedures with verification steps
- Validate data integrity with automated post-migration checks

---

### RISK-003: Performance Requirements
**Keywords**: performance, scalability, load, concurrent, high volume, throughput, latency, SLA  
**Default**: Impact=High(4), Probability=Medium(3), Score=12, Priority=Medium  
**Owner**: Performance Team / DevOps  
**Mitigations**:
- Establish performance baselines early (before feature complete)
- Implement load testing in CI/CD pipeline
- Monitor performance metrics continuously (dashboards + alerts)
- Plan performance optimization buffer in timeline

---

### RISK-004: Security Concerns
**Keywords**: authentication, authorization, security, encrypt, PII, GDPR, compliance, RBAC, SSO, OAuth, password  
**Default**: Impact=Critical(5), Probability=Medium(3), Score=15, Priority=High  
**Owner**: Security Team  
**Mitigations**:
- Conduct security testing with OWASP ZAP or equivalent
- Involve security team in design review before implementation
- Implement automated security scans in CI/CD
- Perform penetration testing before production release

---

### RISK-005: Large Epic Scope
**Condition**: story_count > 30 OR total_story_points > 150  
**Default**: Impact=High(4), Probability=High(4), Score=16, Priority=High  
**Owner**: Product Owner / Engineering Manager  
**Mitigations**:
- Break Epic into smaller delivery milestones
- Implement incremental testing approach (test-as-you-go)
- Consider increasing test team size or extending timeline
- Prioritize critical path testing over exhaustive coverage

---

### RISK-006: Incomplete Requirements
**Condition**: no child stories linked OR empty epic description  
**Default**: Impact=High(4), Probability=High(4), Score=16, Priority=High  
**Owner**: Product Owner  
**Mitigations**:
- Schedule requirements refinement sessions immediately
- Create detailed acceptance criteria for each story
- Conduct 3-amigos sessions (Dev + QA + PO) before sprint start
- Document assumptions and get explicit sign-off

---

### RISK-007: External Dependencies
**Keywords** (in story summaries/descriptions): depends on, blocked by, waiting for, requires team  
**Condition**: detected in > 3 stories  
**Default**: Impact=Medium(3), Probability=High(4), Score=12, Priority=Medium  
**Owner**: Scrum Master / Tech Lead  
**Mitigations**:
- Map all dependencies explicitly in planning
- Establish clear communication channels and SLAs with dependent teams
- Use stubs/mocks to unblock testing from external dependencies
- Track dependency status in daily standups

---

### RISK-008: New Technology or Framework
**Keywords**: new framework, first time, prototype, experiment, POC, proof of concept, unfamiliar  
**Default**: Impact=High(4), Probability=Medium(3), Score=12, Priority=Medium  
**Owner**: Tech Lead  
**Mitigations**:
- Conduct technology spike or POC before sprint start
- Provide training or pairing sessions for the team
- Allow extra time buffer for learning curve (30–50% overhead)
- Engage vendor support or community if applicable

---

## Risk matrix

```
     Impact →
Prob.   Negligible  Low    Medium  High   Critical
↓       (1)         (2)    (3)     (4)    (5)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
V.High  5          10     15      20     25   ← 20+ = Critical
(5)
High    4           8     12      16     20   ← 15-19 = High
(4)
Medium  3           6      9      12     15   ← 9-14 = Medium
(3)
Low     2           4      6       8     10   ← < 9 = Low
(2)
V.Low   1           2      3       4      5
(1)
```
