# Java + Playwright — POM Templates

## Required dependencies (Maven)

```xml
<dependency>
  <groupId>com.microsoft.playwright</groupId>
  <artifactId>playwright</artifactId>
  <version>1.x.x</version>
</dependency>
```

---

## Base page class

```java
import com.microsoft.playwright.Page;
import com.microsoft.playwright.Locator;
import com.microsoft.playwright.options.AriaRole;

public abstract class BasePage {

    protected final Page page;

    public BasePage(Page page) {
        this.page = page;
    }

    protected void navigateTo(String url) {
        page.navigate(url);
    }

    protected String getTitle() {
        return page.title();
    }

    protected void waitForLoad() {
        page.waitForLoadState();
    }
}
```

---

## POM class template

In Playwright Java, locators are lazy — they are evaluated at interaction time,
not at construction. Define locators as methods or fields returning `Locator`.
Prefer semantic locators (`getByRole`, `getByLabel`, `getByTestId`) over
raw CSS/XPath for resilience.

```java
import com.microsoft.playwright.Page;
import com.microsoft.playwright.Locator;
import com.microsoft.playwright.options.AriaRole;

public class [PageName]Page extends BasePage {

    // --- Locator accessors ------------------------------------------------
    // Return Locator from a method so they stay lazy and composable.

    private Locator someInput() {
        return page.getByLabel("Field label");
    }

    private Locator submitButton() {
        return page.getByRole(AriaRole.BUTTON, new Page.GetByRoleOptions().setName("Submit"));
    }

    private Locator errorMessage() {
        return page.locator(".error-message");
    }

    // --- Constructor -------------------------------------------------------

    public [PageName]Page(Page page) {
        super(page);
    }

    // --- Action methods ---------------------------------------------------

    public [PageName]Page enterValue(String value) {
        someInput().fill(value);
        return this;
    }

    public NextPage clickSubmit() {
        submitButton().click();
        return new NextPage(page);
    }

    // --- State / verification methods ------------------------------------

    public String getErrorMessage() {
        return errorMessage().textContent();
    }

    public boolean isErrorVisible() {
        return errorMessage().isVisible();
    }

    public boolean isSubmitEnabled() {
        return submitButton().isEnabled();
    }
}
```

---

## Locator strategy cheatsheet

| Strategy           | Java API                                                                             |
|--------------------|--------------------------------------------------------------------------------------|
| By ARIA role       | `page.getByRole(AriaRole.BUTTON, new Page.GetByRoleOptions().setName("Login"))`      |
| By label           | `page.getByLabel("Email address")`                                                   |
| By placeholder     | `page.getByPlaceholder("Enter your email")`                                          |
| By test ID         | `page.getByTestId("submit-btn")`                                                     |
| By text            | `page.getByText("Sign in")`                                                          |
| By CSS             | `page.locator("button[type='submit']")`                                              |
| By XPath           | `page.locator("xpath=//button[@type='submit']")`                                     |
| Nth match          | `page.locator(".item").nth(2)`                                                       |
| Chained / filter   | `page.locator(".list").filter(new Locator.FilterOptions().setHasText("Active"))`     |

---

## Element interaction cheatsheet

| Interaction       | Playwright API                         |
|-------------------|----------------------------------------|
| Fill text field   | `locator.fill("value")`                |
| Click             | `locator.click()`                      |
| Check checkbox    | `locator.check()`                      |
| Uncheck checkbox  | `locator.uncheck()`                    |
| Select dropdown   | `locator.selectOption("value")`        |
| Get text          | `locator.textContent()`                |
| Get input value   | `locator.inputValue()`                 |
| Is visible        | `locator.isVisible()`                  |
| Is enabled        | `locator.isEnabled()`                  |
| Wait for visible  | `locator.waitFor()`                    |
| Hover             | `locator.hover()`                      |
| Press key         | `locator.press("Enter")`               |

---

## Worked example — Login page

```java
import com.microsoft.playwright.Page;
import com.microsoft.playwright.Locator;
import com.microsoft.playwright.options.AriaRole;

public class LoginPage extends BasePage {

    public LoginPage(Page page) {
        super(page);
    }

    // Locators as private methods — lazy, composable, easy to update
    private Locator emailInput()          { return page.getByLabel("Email"); }
    private Locator passwordInput()       { return page.getByLabel("Password"); }
    private Locator loginButton()         { return page.getByRole(AriaRole.BUTTON, new Page.GetByRoleOptions().setName("Log in")); }
    private Locator errorBanner()         { return page.locator("[role='alert']"); }
    private Locator forgotPasswordLink()  { return page.getByText("Forgot your password?"); }

    public LoginPage enterEmail(String email) {
        emailInput().fill(email);
        return this;
    }

    public LoginPage enterPassword(String password) {
        passwordInput().fill(password);
        return this;
    }

    public DashboardPage clickLogin() {
        loginButton().click();
        return new DashboardPage(page);
    }

    public LoginPage clickLoginExpectingFailure() {
        loginButton().click();
        return this;
    }

    public ForgotPasswordPage clickForgotPassword() {
        forgotPasswordLink().click();
        return new ForgotPasswordPage(page);
    }

    public String getErrorMessage() {
        return errorBanner().textContent();
    }

    public boolean isErrorVisible() {
        return errorBanner().isVisible();
    }
}
```

**Example test:**
```java
@Test
void loginWithValidCredentials(Page page) {
    LoginPage loginPage = new LoginPage(page);
    DashboardPage dashboard = loginPage
        .enterEmail("user@example.com")
        .enterPassword("secret123")
        .clickLogin();
    assertTrue(dashboard.isWelcomeMessageVisible());
}
```
