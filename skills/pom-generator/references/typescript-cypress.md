# TypeScript + Cypress — POM Templates

## Required packages

```bash
npm install -D cypress
npm install -D @types/cypress   # usually not needed — Cypress ships its own types
```

`tsconfig.json` should include:
```json
{
  "compilerOptions": {
    "target": "ES6",
    "lib": ["ES6", "DOM"],
    "types": ["cypress"]
  }
}
```

---

## Two valid POM approaches in Cypress

### Approach 1: Class-based POM (recommended for TypeScript)

Typed class where methods wrap `cy` commands. Provides autocompletion and
catches typos at compile time.

```typescript
// cypress/pages/[page-name]-page.ts

export class [PageName]Page {

  // --- Locator getters --------------------------------------------------
  // Return Cypress.Chainable — don't store as variables.

  get someInput():    Cypress.Chainable { return cy.get('#element-id'); }
  get submitButton(): Cypress.Chainable { return cy.get("button[type='submit']"); }
  get errorMessage(): Cypress.Chainable { return cy.get('.error-message'); }

  // --- Action methods ---------------------------------------------------

  enterValue(value: string): this {
    this.someInput.clear().type(value);
    return this;
  }

  clickSubmit(): void {
    this.submitButton.click();
  }

  // --- Assertion helpers -----------------------------------------------

  shouldShowError(message: string): void {
    this.errorMessage.should('be.visible').and('contain.text', message);
  }

  shouldNotShowError(): void {
    this.errorMessage.should('not.exist');
  }
}
```

### Approach 2: Custom commands with types

Extend Cypress's `Chainable` interface for IDE support:

```typescript
// cypress/support/commands.ts

Cypress.Commands.add('login', (email: string, password: string) => {
  cy.get('#email').type(email);
  cy.get('#password').type(password);
  cy.get("button[type='submit']").click();
});

// cypress/support/index.d.ts
declare namespace Cypress {
  interface Chainable {
    login(email: string, password: string): Chainable<void>;
  }
}
```

**Recommendation**: Use the class-based approach for pages with many elements
and team-wide adoption. Use custom commands for cross-page flows (login, auth).

---

## Locator strategy cheatsheet

| Strategy          | TypeScript / Cypress                                   |
|-------------------|--------------------------------------------------------|
| By ID             | `cy.get('#element-id')`                                |
| By CSS            | `cy.get("button[type='submit']")`                      |
| By data-cy attr   | `cy.get('[data-cy="submit-btn"]')`                     |
| By data-testid    | `cy.get('[data-testid="submit-btn"]')`                 |
| By text content   | `cy.contains('Submit')`                                |
| By role           | `cy.get('[role="button"]')`                            |
| By name attr      | `cy.get('[name="username"]')`                          |
| Nth match         | `cy.get('.item').eq(2)`                                |
| Child element     | `cy.get('.form').find('input')`                        |

---

## Interaction cheatsheet

| Interaction         | Cypress                                    |
|---------------------|--------------------------------------------|
| Type into input     | `.type('value')`                           |
| Clear and type      | `.clear().type('value')`                   |
| Click               | `.click()`                                 |
| Check checkbox      | `.check()`                                 |
| Uncheck checkbox    | `.uncheck()`                               |
| Select dropdown     | `.select('option-value')`                  |
| Get text            | `.invoke('text')`                          |
| Assert visible      | `.should('be.visible')`                    |
| Assert text         | `.should('contain.text', 'Expected')`      |
| Assert enabled      | `.should('be.enabled')`                    |
| Assert count        | `.should('have.length', 3)`                |

---

## Worked example — Login page

```typescript
// cypress/pages/login-page.ts

export class LoginPage {

  get emailInput():        Cypress.Chainable { return cy.get('#email'); }
  get passwordInput():     Cypress.Chainable { return cy.get('#password'); }
  get loginButton():       Cypress.Chainable { return cy.get("button[type='submit']"); }
  get errorBanner():       Cypress.Chainable { return cy.get('.auth-error'); }
  get forgotPasswordLink(): Cypress.Chainable { return cy.contains('Forgot your password?'); }

  visit(): this {
    cy.visit('/login');
    return this;
  }

  enterEmail(email: string): this {
    this.emailInput.clear().type(email);
    return this;
  }

  enterPassword(password: string): this {
    this.passwordInput.clear().type(password);
    return this;
  }

  clickLogin(): void {
    this.loginButton.click();
  }

  clickForgotPassword(): void {
    this.forgotPasswordLink.click();
  }

  shouldShowError(message: string): void {
    this.errorBanner.should('be.visible').and('contain.text', message);
  }

  shouldNotShowError(): void {
    this.errorBanner.should('not.exist');
  }
}
```

**Example test:**
```typescript
// cypress/e2e/login.cy.ts
import { LoginPage } from '../pages/login-page';

const loginPage = new LoginPage();

describe('Login', () => {
  beforeEach(() => loginPage.visit());

  it('logs in with valid credentials', () => {
    loginPage
      .enterEmail('user@example.com')
      .enterPassword('secret123')
      .clickLogin();
    cy.url().should('include', '/dashboard');
  });

  it('shows error for invalid credentials', () => {
    loginPage
      .enterEmail('bad@example.com')
      .enterPassword('wrong')
      .clickLogin();
    loginPage.shouldShowError('Invalid email or password');
  });
});
```
