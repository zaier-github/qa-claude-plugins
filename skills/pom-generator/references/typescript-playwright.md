# TypeScript + Playwright — POM Templates

This is Playwright's recommended language/framework combination. Uses the
fixture-based pattern from `@playwright/test`.

## Required packages

```bash
npm install -D @playwright/test
npx playwright install
```

---

## Base page class

```typescript
import { Page, Locator } from '@playwright/test';

export abstract class BasePage {
  readonly page: Page;

  constructor(page: Page) {
    this.page = page;
  }

  async navigate(url: string): Promise<void> {
    await this.page.goto(url);
  }

  async title(): Promise<string> {
    return this.page.title();
  }

  async waitForLoad(): Promise<void> {
    await this.page.waitForLoadState('networkidle');
  }
}
```

---

## POM class template

Define locators as `readonly` properties using `Locator`. Prefer
`getByRole`, `getByLabel`, `getByTestId` over CSS for resilience.
Action methods are `async` and return `this` or the next page object.

```typescript
import { Page, Locator } from '@playwright/test';
import { BasePage } from './base-page';
import { NextPage } from './next-page';

export class [PageName]Page extends BasePage {

  // --- Locators ----------------------------------------------------------
  readonly someInput: Locator;
  readonly submitButton: Locator;
  readonly errorMessage: Locator;

  constructor(page: Page) {
    super(page);
    this.someInput    = page.getByLabel('Field label');
    this.submitButton = page.getByRole('button', { name: 'Submit' });
    this.errorMessage = page.locator('.error-message');
  }

  // --- Action methods ---------------------------------------------------

  async enterValue(value: string): Promise<this> {
    await this.someInput.fill(value);
    return this;
  }

  async clickSubmit(): Promise<NextPage> {
    await this.submitButton.click();
    return new NextPage(this.page);
  }

  // --- State / verification methods ------------------------------------

  async getErrorMessage(): Promise<string> {
    return (await this.errorMessage.textContent()) ?? '';
  }

  async isErrorVisible(): Promise<boolean> {
    return this.errorMessage.isVisible();
  }

  async isSubmitEnabled(): Promise<boolean> {
    return this.submitButton.isEnabled();
  }
}
```

---

## Locator strategy cheatsheet

| Strategy           | TypeScript                                                    |
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
| Child locator      | `page.locator('.form').locator('input')`                      |

---

## Fixture-based pattern (recommended for test files)

Rather than constructing page objects manually, extend Playwright's test fixture:

```typescript
// fixtures.ts
import { test as base } from '@playwright/test';
import { LoginPage } from './pages/login-page';
import { DashboardPage } from './pages/dashboard-page';

type Pages = {
  loginPage: LoginPage;
  dashboardPage: DashboardPage;
};

export const test = base.extend<Pages>({
  loginPage: async ({ page }, use) => {
    await use(new LoginPage(page));
  },
  dashboardPage: async ({ page }, use) => {
    await use(new DashboardPage(page));
  },
});

export { expect } from '@playwright/test';
```

Then in tests:
```typescript
import { test, expect } from './fixtures';

test('login with valid credentials', async ({ loginPage }) => {
  await loginPage.navigate('/login');
  const dashboard = await loginPage
    .enterEmail('user@example.com')
    .then(p => p.enterPassword('secret123'))
    .then(p => p.clickLogin());
  expect(await dashboard.isWelcomeMessageVisible()).toBe(true);
});
```

---

## Worked example — Login page

```typescript
import { Page, Locator } from '@playwright/test';
import { BasePage } from './base-page';
import { DashboardPage } from './dashboard-page';
import { ForgotPasswordPage } from './forgot-password-page';

export class LoginPage extends BasePage {

  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly loginButton: Locator;
  readonly errorBanner: Locator;
  readonly forgotPasswordLink: Locator;

  constructor(page: Page) {
    super(page);
    this.emailInput        = page.getByLabel('Email');
    this.passwordInput     = page.getByLabel('Password');
    this.loginButton       = page.getByRole('button', { name: 'Log in' });
    this.errorBanner       = page.locator('[role="alert"]');
    this.forgotPasswordLink = page.getByText('Forgot your password?');
  }

  async enterEmail(email: string): Promise<this> {
    await this.emailInput.fill(email);
    return this;
  }

  async enterPassword(password: string): Promise<this> {
    await this.passwordInput.fill(password);
    return this;
  }

  async clickLogin(): Promise<DashboardPage> {
    await this.loginButton.click();
    return new DashboardPage(this.page);
  }

  async clickLoginExpectingFailure(): Promise<this> {
    await this.loginButton.click();
    return this;
  }

  async clickForgotPassword(): Promise<ForgotPasswordPage> {
    await this.forgotPasswordLink.click();
    return new ForgotPasswordPage(this.page);
  }

  async getErrorMessage(): Promise<string> {
    return (await this.errorBanner.textContent()) ?? '';
  }

  async isErrorVisible(): Promise<boolean> {
    return this.errorBanner.isVisible();
  }
}
```
