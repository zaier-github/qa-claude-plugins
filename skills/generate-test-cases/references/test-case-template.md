# Test Case Template

Use this template for each test case block in `test-cases-{KEY}.md`.

---

```markdown
---
id: TC-PROJ-123-001
summary: Verify successful login with valid credentials
requirementKey: PROJ-123
testType: Manual
priority: P1
type: Happy Path
regressionSuite: true
riskLevel: High
effort: Medium
tags: [login, auth, regression]
businessRules: [BR-001]
estimatedDuration: 5 minutes
language: en
---

# TC-PROJ-123-001: Verify successful login with valid credentials

## Test Objective
Validate that a registered user can log in with valid credentials and be redirected to the dashboard.

## User Story Reference
**Story**: PROJ-123 — User Authentication  
**Requirement Key**: PROJ-123  
**Acceptance Criteria**: AC-001 (User can log in with valid email and password)

## Business Rules Covered
- BR-001: Users must authenticate before accessing any protected resource

## Prerequisites
- A registered user account exists in the system
- The application is deployed and accessible
- Test user credentials are available

## Test Data Requirements

| Data Element | Value | Notes |
|---|---|---|
| Email | `test.user@company.com` | Valid registered user |
| Password | `TestPass123!` | Meets password complexity policy |
| Expected redirect | `/dashboard` | Post-login URL |

## Test Steps

### Setup
1. Clear browser cache and cookies
2. Navigate to the application base URL

### Execution
1. **Navigate** to the login page at `/login`  
   → *Expected*: Login form displays with email, password fields and a Login button

2. **Enter** `<VALID_EMAIL>` in the Email field  
   → *Expected*: Email is accepted, no validation error

3. **Enter** `<VALID_PASSWORD>` in the Password field  
   → *Expected*: Password is masked, no validation error

4. **Click** the "Login" button  
   → *Expected*: Loading indicator appears; authentication begins

5. **Verify** the user is redirected to `/dashboard`  
   → *Expected*: Dashboard page loads with user-specific content and correct username displayed

## Expected Results
- User is authenticated successfully
- Dashboard displays the correct user's name and personalized content
- A valid session cookie is set
- No error messages appear

## Postconditions
- User is logged in with an active session
- User can navigate to protected routes

## Traceability
- **Requirement**: PROJ-123
- **Acceptance Criteria**: AC-001
- **Related tests**: TC-PROJ-123-002 (invalid login), TC-PROJ-123-003 (session timeout)
```
