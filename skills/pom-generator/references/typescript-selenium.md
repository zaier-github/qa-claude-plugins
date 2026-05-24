# TypeScript + Selenium WebDriver — POM Templates

## Required packages

```bash
npm install selenium-webdriver
npm install -D @types/selenium-webdriver typescript ts-node
```

---

## Base page class

```typescript
// base-page.ts
import { WebDriver, By, Locator, until, WebElement } from 'selenium-webdriver';

export abstract class BasePage {
  protected driver: WebDriver;
  protected timeout: number;

  constructor(driver: WebDriver, timeout = 10000) {
    this.driver = driver;
    this.timeout = timeout;
  }

  protected async waitForVisible(locator: Locator): Promise<WebElement> {
    const el = await this.driver.wait(until.elementLocated(locator), this.timeout);
    return this.driver.wait(until.elementIsVisible(el), this.timeout);
  }

  protected async clickWhenReady(locator: Locator): Promise<void> {
    const el = await this.driver.wait(until.elementLocated(locator), this.timeout);
    await this.driver.wait(until.elementIsEnabled(el), this.timeout);
    await el.click();
  }

  protected async type(locator: Locator, text: string): Promise<void> {
    const el = await this.waitForVisible(locator);
    await el.clear();
    await el.sendKeys(text);
  }

  protected async getText(locator: Locator): Promise<string> {
    const el = await this.waitForVisible(locator);
    return el.getText();
  }

  protected async isDisplayed(locator: Locator): Promise<boolean> {
    try {
      const el = await this.driver.findElement(locator);
      return el.isDisplayed();
    } catch {
      return false;
    }
  }
}
```

---

## POM class template

```typescript
// [page-name]-page.ts
import { WebDriver, By } from 'selenium-webdriver';
import { BasePage } from './base-page';
import { NextPage } from './next-page';

export class [PageName]Page extends BasePage {

  // --- Locators ----------------------------------------------------------
  private static readonly SOME_INPUT    = By.id('element-id');
  private static readonly SUBMIT_BUTTON = By.css("button[type='submit']");
  private static readonly ERROR_MESSAGE = By.css('.error-message');

  constructor(driver: WebDriver) {
    super(driver);
  }

  // --- Action methods ---------------------------------------------------

  async enterValue(value: string): Promise<this> {
    await this.type([PageName]Page.SOME_INPUT, value);
    return this;
  }

  async clickSubmit(): Promise<NextPage> {
    await this.clickWhenReady([PageName]Page.SUBMIT_BUTTON);
    return new NextPage(this.driver);
  }

  // --- State / verification methods ------------------------------------

  async getErrorMessage(): Promise<string> {
    return this.getText([PageName]Page.ERROR_MESSAGE);
  }

  async isErrorDisplayed(): Promise<boolean> {
    return this.isDisplayed([PageName]Page.ERROR_MESSAGE);
  }

  async isSubmitEnabled(): Promise<boolean> {
    const el = await this.driver.findElement([PageName]Page.SUBMIT_BUTTON);
    return el.isEnabled();
  }
}
```

---

## Locator strategy cheatsheet

| Strategy         | TypeScript                                               |
|------------------|----------------------------------------------------------|
| By ID            | `By.id('element-id')`                                    |
| By name          | `By.name('username')`                                    |
| By CSS selector  | `By.css("button[type='submit']")`                        |
| By XPath         | `By.xpath("//button[@type='submit']")`                   |
| By link text     | `By.linkText('Forgot password?')`                        |
| By class name    | `By.className('error-message')`                          |
| By tag name      | `By.tagName('h1')`                                       |

---

## Worked example — Login page

```typescript
// login-page.ts
import { WebDriver, By } from 'selenium-webdriver';
import { BasePage } from './base-page';
import { DashboardPage } from './dashboard-page';
import { ForgotPasswordPage } from './forgot-password-page';

export class LoginPage extends BasePage {

  private static readonly EMAIL_INPUT     = By.id('email');
  private static readonly PASSWORD_INPUT  = By.id('password');
  private static readonly LOGIN_BUTTON    = By.css("button[type='submit']");
  private static readonly ERROR_BANNER    = By.css('.auth-error');
  private static readonly FORGOT_PWD_LINK = By.linkText('Forgot your password?');

  constructor(driver: WebDriver) {
    super(driver);
  }

  async enterEmail(email: string): Promise<this> {
    await this.type(LoginPage.EMAIL_INPUT, email);
    return this;
  }

  async enterPassword(password: string): Promise<this> {
    await this.type(LoginPage.PASSWORD_INPUT, password);
    return this;
  }

  async clickLogin(): Promise<DashboardPage> {
    await this.clickWhenReady(LoginPage.LOGIN_BUTTON);
    return new DashboardPage(this.driver);
  }

  async clickLoginExpectingFailure(): Promise<this> {
    await this.clickWhenReady(LoginPage.LOGIN_BUTTON);
    return this;
  }

  async clickForgotPassword(): Promise<ForgotPasswordPage> {
    await this.clickWhenReady(LoginPage.FORGOT_PWD_LINK);
    return new ForgotPasswordPage(this.driver);
  }

  async getErrorMessage(): Promise<string> {
    return this.getText(LoginPage.ERROR_BANNER);
  }

  async isErrorDisplayed(): Promise<boolean> {
    return this.isDisplayed(LoginPage.ERROR_BANNER);
  }
}
```

**Example test:**
```typescript
test('login with valid credentials', async () => {
  const dashboard = await new LoginPage(driver)
    .enterEmail('user@example.com')
    .then(p => p.enterPassword('secret123'))
    .then(p => p.clickLogin());
  expect(await dashboard.isWelcomeMessageVisible()).toBe(true);
});
```
