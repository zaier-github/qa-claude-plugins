# JavaScript + Cypress — POM Templates

Cypress has a different philosophy from Selenium/Playwright: commands are
chainable and asynchronous by design. The POM pattern in Cypress is
implemented as **wrapper classes** that return `cy` chains or use custom
commands, rather than async/await classes.

## Required packages

```bash
npm install -D cypress
```

---

## Two valid POM approaches in Cypress

### Approach 1: Class-based POM (closer to Selenium/Playwright style)

Wraps `cy` commands inside methods. Methods don't return `this` directly —
they return Cypress chainables. Use this when migrating from Selenium or when
your team prefers OOP style.

```javascript
// cypress/pages/[page-name]-page.js

class [PageName]Page {

  // --- Locator getters --------------------------------------------------
  // Return cy chainables — don't store elements as variables.

  get someInput()    { return cy.get('#element-id'); }
  get submitButton() { return cy.get("button[type='submit']"); }
  get errorMessage() { return cy.get('.error-message'); }

  // --- Action methods ---------------------------------------------------

  enterValue(value) {
    this.someInput.clear().type(value);
  }

  clickSubmit() {
    this.submitButton.click();
  }

  // --- Assertion helpers -----------------------------------------------
  // In Cypress, verification usually lives in the test via should().
  // Expose element getters so tests can chain assertions directly.

  shouldShowError(message) {
    this.errorMessage.should('be.visible').and('contain.text', message);
  }

  shouldNotShowError() {
    this.errorMessage.should('not.exist');
  }
}

export default [PageName]Page;
```

### Approach 2: Custom commands (idiomatic Cypress)

Add commands to `cy` directly in `cypress/support/commands.js`. More
idiomatic but less structured for large page surfaces.

```javascript
// cypress/support/commands.js

Cypress.Commands.add('login', (email, password) => {
  cy.get('#email').type(email);
  cy.get('#password').type(password);
  cy.get("button[type='submit']").click();
});

Cypress.Commands.add('getErrorMessage', () => {
  return cy.get('.auth-error');
});
```

**Recommendation**: Use the class-based approach (Approach 1) for complex pages
with many elements. Use custom commands for common cross-page flows (login, auth).

---

## Locator strategy cheatsheet

| Strategy          | Cypress                                                |
|-------------------|--------------------------------------------------------|
| By ID             | `cy.get('#element-id')`                                |
| By CSS            | `cy.get("button[type='submit']")`                      |
| By data-cy attr   | `cy.get('[data-cy="submit-btn"]')`                     |
| By data-testid    | `cy.get('[data-testid="submit-btn"]')` or `cy.getByTestId` (if Testing Library installed) |
| By text content   | `cy.contains('Submit')`                                |
| By role           | `cy.get('[role="button"]')`                            |
| By name attr      | `cy.get('[name="username"]')`                          |
| Nth match         | `cy.get('.item').eq(2)`                                |
| Child element     | `cy.get('.form').find('input')`                        |
| Filter by text    | `cy.get('.row').contains('Active')`                    |

---

## Element interaction cheatsheet

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

```javascript
// cypress/pages/login-page.js

class LoginPage {

  get emailInput()       { return cy.get('#email'); }
  get passwordInput()    { return cy.get('#password'); }
  get loginButton()      { return cy.get("button[type='submit']"); }
  get errorBanner()      { return cy.get('.auth-error'); }
  get forgotPasswordLink() { return cy.contains('Forgot your password?'); }

  visit() {
    cy.visit('/login');
  }

  enterEmail(email) {
    this.emailInput.clear().type(email);
  }

  enterPassword(password) {
    this.passwordInput.clear().type(password);
  }

  clickLogin() {
    this.loginButton.click();
  }

  clickForgotPassword() {
    this.forgotPasswordLink.click();
  }

  shouldShowError(message) {
    this.errorBanner.should('be.visible').and('contain.text', message);
  }

  shouldNotShowError() {
    this.errorBanner.should('not.exist');
  }
}

export default LoginPage;
```

**Example test:**
```javascript
// cypress/e2e/login.cy.js
import LoginPage from '../pages/login-page';

const loginPage = new LoginPage();

describe('Login', () => {
  beforeEach(() => loginPage.visit());

  it('logs in with valid credentials', () => {
    loginPage.enterEmail('user@example.com');
    loginPage.enterPassword('secret123');
    loginPage.clickLogin();
    cy.url().should('include', '/dashboard');
  });

  it('shows error for invalid credentials', () => {
    loginPage.enterEmail('bad@example.com');
    loginPage.enterPassword('wrong');
    loginPage.clickLogin();
    loginPage.shouldShowError('Invalid email or password');
  });
});
```
