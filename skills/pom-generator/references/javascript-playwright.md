# JavaScript + Playwright — POM Templates

## Required packages

```bash
npm install -D @playwright/test
npx playwright install
```

---

## Base page class

```javascript
// base-page.js
class BasePage {
  constructor(page) {
    this.page = page;
  }

  async navigate(url) {
    await this.page.goto(url);
  }

  async title() {
    return this.page.title();
  }

  async waitForLoad() {
    await this.page.waitForLoadState('networkidle');
  }
}

module.exports = { BasePage };
```

---

## POM class template

```javascript
// [page-name]-page.js
const { BasePage } = require('./base-page');

class [PageName]Page extends BasePage {

  constructor(page) {
    super(page);
    // Define locators in the constructor so they're available on `this`.
    // Prefer semantic locators (getByRole, getByLabel) over CSS.
    this.someInput    = page.getByLabel('Field label');
    this.submitButton = page.getByRole('button', { name: 'Submit' });
    this.errorMessage = page.locator('.error-message');
  }

  // --- Action methods ---------------------------------------------------

  async enterValue(value) {
    await this.someInput.fill(value);
    return this;
  }

  async clickSubmit() {
    await this.submitButton.click();
    const { NextPage } = require('./next-page');
    return new NextPage(this.page);
  }

  // --- State / verification methods ------------------------------------

  async getErrorMessage() {
    return this.errorMessage.textContent();
  }

  async isErrorVisible() {
    return this.errorMessage.isVisible();
  }

  async isSubmitEnabled() {
    return this.submitButton.isEnabled();
  }
}

module.exports = { [PageName]Page };
```

---

## Locator strategy cheatsheet

| Strategy           | JavaScript                                                    |
|--------------------|---------------------------------------------------------------|
| By ARIA role       | `page.getByRole('button', { name: 'Login' })`                 |
| By label           | `page.getByLabel('Email address')`                            |
| By placeholder     | `page.getByPlaceholder('Enter your email')`                   |
| By test ID         | `page.getByTestId('submit-btn')`                              |
| By text            | `page.getByText('Sign in')`                                   |
| By CSS             | `page.locator('button[type="submit"]')`                       |
| By XPath           | `page.locator('xpath=//button[@type="submit"]')`              |
| Nth match          | `page.locator('.item').nth(2)`                                |
| Filter by text     | `page.locator('.row').filter({ hasText: 'Active' })`          |

---

## Worked example — Login page

```javascript
// login-page.js
const { BasePage } = require('./base-page');

class LoginPage extends BasePage {

  constructor(page) {
    super(page);
    this.emailInput        = page.getByLabel('Email');
    this.passwordInput     = page.getByLabel('Password');
    this.loginButton       = page.getByRole('button', { name: 'Log in' });
    this.errorBanner       = page.locator('[role="alert"]');
    this.forgotPasswordLink = page.getByText('Forgot your password?');
  }

  async enterEmail(email) {
    await this.emailInput.fill(email);
    return this;
  }

  async enterPassword(password) {
    await this.passwordInput.fill(password);
    return this;
  }

  async clickLogin() {
    await this.loginButton.click();
    const { DashboardPage } = require('./dashboard-page');
    return new DashboardPage(this.page);
  }

  async clickLoginExpectingFailure() {
    await this.loginButton.click();
    return this;
  }

  async clickForgotPassword() {
    await this.forgotPasswordLink.click();
    const { ForgotPasswordPage } = require('./forgot-password-page');
    return new ForgotPasswordPage(this.page);
  }

  async getErrorMessage() {
    return this.errorBanner.textContent();
  }

  async isErrorVisible() {
    return this.errorBanner.isVisible();
  }
}

module.exports = { LoginPage };
```

**Example test:**
```javascript
const { test, expect } = require('@playwright/test');
const { LoginPage } = require('./pages/login-page');

test('login with valid credentials', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.navigate('/login');
  const dashboard = await (await loginPage.enterEmail('user@example.com'))
    .enterPassword('secret123')
    .then(p => p.clickLogin());
  expect(await dashboard.isWelcomeMessageVisible()).toBe(true);
});
```
