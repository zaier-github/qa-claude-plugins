# Java + Selenium WebDriver — POM Templates

## Required dependencies (Maven)

```xml
<dependency>
  <groupId>org.seleniumhq.selenium</groupId>
  <artifactId>selenium-java</artifactId>
  <version>4.x.x</version>
</dependency>
```

---

## Base page class

Generate this once per project when the user requests it. All page classes extend it.

```java
import org.openqa.selenium.*;
import org.openqa.selenium.support.PageFactory;
import org.openqa.selenium.support.ui.*;
import java.time.Duration;

public abstract class BasePage {

    protected WebDriver driver;
    protected WebDriverWait wait;

    public BasePage(WebDriver driver) {
        this.driver = driver;
        this.wait = new WebDriverWait(driver, Duration.ofSeconds(10));
        PageFactory.initElements(driver, this);
    }

    protected void waitForVisible(WebElement element) {
        wait.until(ExpectedConditions.visibilityOf(element));
    }

    protected void clickWhenReady(WebElement element) {
        wait.until(ExpectedConditions.elementToBeClickable(element)).click();
    }

    protected void type(WebElement element, String text) {
        waitForVisible(element);
        element.clear();
        element.sendKeys(text);
    }

    protected String getText(WebElement element) {
        waitForVisible(element);
        return element.getText();
    }

    protected boolean isDisplayed(WebElement element) {
        try {
            return element.isDisplayed();
        } catch (NoSuchElementException e) {
            return false;
        }
    }
}
```

---

## POM class template

Use `@FindBy` annotations when possible — they are initialized by `PageFactory`
in the `BasePage` constructor. Fall back to `driver.findElement()` only for
dynamic locators (e.g., table rows keyed by runtime data).

```java
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.How;

public class [PageName]Page extends BasePage {

    // --- Element locators -------------------------------------------------
    // Prefer @FindBy for static elements; driver.findElement() for dynamic ones.

    @FindBy(id = "element-id")
    private WebElement someInput;

    @FindBy(css = "button[type='submit']")
    private WebElement submitButton;

    @FindBy(xpath = "//span[contains(@class,'error')]")
    private WebElement errorMessage;

    // --- Constructor -------------------------------------------------------

    public [PageName]Page(WebDriver driver) {
        super(driver);
    }

    // --- Action methods ---------------------------------------------------
    // Name methods after the user action, not the element.
    // Return `this` for chainable calls, or the next page object for navigations.

    public [PageName]Page enterValue(String value) {
        type(someInput, value);
        return this;
    }

    public NextPage clickSubmit() {
        clickWhenReady(submitButton);
        return new NextPage(driver);
    }

    // --- State / verification methods ------------------------------------
    // Return data or booleans — never assert here.

    public String getErrorMessage() {
        return getText(errorMessage);
    }

    public boolean isErrorDisplayed() {
        return isDisplayed(errorMessage);
    }

    public boolean isSubmitEnabled() {
        return submitButton.isEnabled();
    }
}
```

---

## Element pattern cheatsheet

| Element type       | @FindBy example                                      | Interaction                        |
|--------------------|------------------------------------------------------|------------------------------------|
| Text input         | `@FindBy(id = "username")`                           | `type(el, text)`                   |
| Password field     | `@FindBy(name = "password")`                         | `type(el, text)`                   |
| Submit button      | `@FindBy(css = "button[type='submit']")`             | `clickWhenReady(el)`               |
| Link               | `@FindBy(linkText = "Forgot password?")`             | `clickWhenReady(el)`               |
| Checkbox           | `@FindBy(id = "remember-me")`                        | `el.click()` if not checked        |
| Dropdown (Select)  | `@FindBy(id = "country")`                            | `new Select(el).selectByValue(v)`  |
| Error message      | `@FindBy(css = ".error-message")`                    | `getText(el)`                       |
| Alert/toast        | `@FindBy(css = "[role='alert']")`                    | `getText(el)`                       |
| Dynamic row by text| *(use driver.findElement at call time)*              | `driver.findElement(By.xpath(...))` |

---

## Worked example — Login page

```java
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;

public class LoginPage extends BasePage {

    @FindBy(id = "email")
    private WebElement emailInput;

    @FindBy(id = "password")
    private WebElement passwordInput;

    @FindBy(css = "button[type='submit']")
    private WebElement loginButton;

    @FindBy(css = ".auth-error")
    private WebElement errorBanner;

    @FindBy(linkText = "Forgot your password?")
    private WebElement forgotPasswordLink;

    public LoginPage(WebDriver driver) {
        super(driver);
    }

    public LoginPage enterEmail(String email) {
        type(emailInput, email);
        return this;
    }

    public LoginPage enterPassword(String password) {
        type(passwordInput, password);
        return this;
    }

    public DashboardPage clickLogin() {
        clickWhenReady(loginButton);
        return new DashboardPage(driver);
    }

    public LoginPage clickLoginExpectingFailure() {
        clickWhenReady(loginButton);
        return this;
    }

    public ForgotPasswordPage clickForgotPassword() {
        clickWhenReady(forgotPasswordLink);
        return new ForgotPasswordPage(driver);
    }

    public String getErrorMessage() {
        return getText(errorBanner);
    }

    public boolean isErrorDisplayed() {
        return isDisplayed(errorBanner);
    }
}
```

**Example test using this POM:**
```java
@Test
public void loginWithValidCredentials() {
    LoginPage loginPage = new LoginPage(driver);
    DashboardPage dashboard = loginPage
        .enterEmail("user@example.com")
        .enterPassword("secret123")
        .clickLogin();
    assertTrue(dashboard.isWelcomeMessageVisible());
}
```
