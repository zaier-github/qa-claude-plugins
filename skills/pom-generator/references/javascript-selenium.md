# JavaScript + Selenium WebDriver — POM Templates

## Required packages

```bash
npm install selenium-webdriver
```

---

## Base page class

```javascript
// base-page.js
const { until, By } = require('selenium-webdriver');

class BasePage {
  constructor(driver, timeout = 10000) {
    this.driver = driver;
    this.timeout = timeout;
  }

  async waitForVisible(locator) {
    return this.driver.wait(until.elementLocated(locator), this.timeout)
      .then(el => this.driver.wait(until.elementIsVisible(el), this.timeout));
  }

  async clickWhenReady(locator) {
    const el = await this.driver.wait(until.elementLocated(locator), this.timeout);
    await this.driver.wait(until.elementIsEnabled(el), this.timeout);
    await el.click();
  }

  async type(locator, text) {
    const el = await this.waitForVisible(locator);
    await el.clear();
    await el.sendKeys(text);
  }

  async getText(locator) {
    const el = await this.waitForVisible(locator);
    return el.getText();
  }

  async isDisplayed(locator) {
    try {
      const el = await this.driver.findElement(locator);
      return el.isDisplayed();
    } catch {
      return false;
    }
  }
}

module.exports = { BasePage };
```

---

## POM class template

```javascript
// [page-name]-page.js
const { By } = require('selenium-webdriver');
const { BasePage } = require('./base-page');

class [PageName]Page extends BasePage {

  // Define locators as static/instance properties using By.
  static SOME_INPUT    = By.id('element-id');
  static SUBMIT_BUTTON = By.css("button[type='submit']");
  static ERROR_MESSAGE = By.css('.error-message');

  constructor(driver) {
    super(driver);
  }

  // --- Action methods ---------------------------------------------------

  async enterValue(value) {
    await this.type([PageName]Page.SOME_INPUT, value);
    return this;
  }

  async clickSubmit() {
    await this.clickWhenReady([PageName]Page.SUBMIT_BUTTON);
    const { NextPage } = require('./next-page');
    return new NextPage(this.driver);
  }

  // --- State / verification methods ------------------------------------

  async getErrorMessage() {
    return this.getText([PageName]Page.ERROR_MESSAGE);
  }

  async isErrorDisplayed() {
    return this.isDisplayed([PageName]Page.ERROR_MESSAGE);
  }

  async isSubmitEnabled() {
    const el = await this.driver.findElement([PageName]Page.SUBMIT_BUTTON);
    return el.isEnabled();
  }
}

module.exports = { [PageName]Page };
```

---

## Locator strategy cheatsheet

| Strategy         | JavaScript                                            |
|------------------|-------------------------------------------------------|
| By ID            | `By.id('element-id')`                                 |
| By name          | `By.name('username')`                                 |
| By CSS selector  | `By.css("button[type='submit']")`                     |
| By XPath         | `By.xpath("//button[@type='submit']")`                |
| By link text     | `By.linkText('Forgot password?')`                     |
| By class name    | `By.className('error-message')`                       |
| By tag name      | `By.tagName('h1')`                                    |

---

## Worked example — Login page

```javascript
// login-page.js
const { By } = require('selenium-webdriver');
const { BasePage } = require('./base-page');

class LoginPage extends BasePage {

  static EMAIL_INPUT      = By.id('email');
  static PASSWORD_INPUT   = By.id('password');
  static LOGIN_BUTTON     = By.css("button[type='submit']");
  static ERROR_BANNER     = By.css('.auth-error');
  static FORGOT_PWD_LINK  = By.linkText('Forgot your password?');

  constructor(driver) {
    super(driver);
  }

  async enterEmail(email) {
    await this.type(LoginPage.EMAIL_INPUT, email);
    return this;
  }

  async enterPassword(password) {
    await this.type(LoginPage.PASSWORD_INPUT, password);
    return this;
  }

  async clickLogin() {
    await this.clickWhenReady(LoginPage.LOGIN_BUTTON);
    const { DashboardPage } = require('./dashboard-page');
    return new DashboardPage(this.driver);
  }

  async clickLoginExpectingFailure() {
    await this.clickWhenReady(LoginPage.LOGIN_BUTTON);
    return this;
  }

  async clickForgotPassword() {
    await this.clickWhenReady(LoginPage.FORGOT_PWD_LINK);
    const { ForgotPasswordPage } = require('./forgot-password-page');
    return new ForgotPasswordPage(this.driver);
  }

  async getErrorMessage() {
    return this.getText(LoginPage.ERROR_BANNER);
  }

  async isErrorDisplayed() {
    return this.isDisplayed(LoginPage.ERROR_BANNER);
  }
}

module.exports = { LoginPage };
```
