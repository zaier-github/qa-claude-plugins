# Python + Selenium WebDriver — POM Templates

## Required packages

```bash
pip install selenium
```

---

## Base page class

```python
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


class BasePage:
    def __init__(self, driver: WebDriver, timeout: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def _wait_for_visible(self, locator: tuple) -> WebElement:
        return self.wait.until(EC.visibility_of_element_located(locator))

    def _click_when_ready(self, locator: tuple) -> None:
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def _type(self, locator: tuple, text: str) -> None:
        element = self._wait_for_visible(locator)
        element.clear()
        element.send_keys(text)

    def _get_text(self, locator: tuple) -> str:
        return self._wait_for_visible(locator).text

    def _is_displayed(self, locator: tuple) -> bool:
        try:
            return self.driver.find_element(*locator).is_displayed()
        except NoSuchElementException:
            return False
```

---

## POM class template

Define locators as class-level tuples using `By`. Expose interactions as
methods named after the user action. Return `self` for fluent chaining, or
the next page object for navigation actions.

```python
from selenium.webdriver.common.by import By
from .base_page import BasePage


class [PageName]Page(BasePage):

    # --- Locators ---------------------------------------------------------
    # Define as class-level constants so they're easy to update in one place.

    _SOME_INPUT    = (By.ID, "element-id")
    _SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    _ERROR_MESSAGE = (By.CSS_SELECTOR, ".error-message")

    # --- Action methods ---------------------------------------------------

    def enter_value(self, value: str) -> "[PageName]Page":
        self._type(self._SOME_INPUT, value)
        return self

    def click_submit(self) -> "NextPage":
        self._click_when_ready(self._SUBMIT_BUTTON)
        from .next_page import NextPage
        return NextPage(self.driver)

    # --- State / verification methods ------------------------------------

    def get_error_message(self) -> str:
        return self._get_text(self._ERROR_MESSAGE)

    def is_error_displayed(self) -> bool:
        return self._is_displayed(self._ERROR_MESSAGE)

    def is_submit_enabled(self) -> bool:
        return self.driver.find_element(*self._SUBMIT_BUTTON).is_enabled()
```

---

## Locator strategy cheatsheet

| Strategy         | Python                                             |
|------------------|----------------------------------------------------|
| By ID            | `(By.ID, "element-id")`                            |
| By name          | `(By.NAME, "username")`                            |
| By CSS selector  | `(By.CSS_SELECTOR, "button[type='submit']")`       |
| By XPath         | `(By.XPATH, "//button[@type='submit']")`           |
| By link text     | `(By.LINK_TEXT, "Forgot password?")`               |
| By partial link  | `(By.PARTIAL_LINK_TEXT, "Forgot")`                 |
| By class name    | `(By.CLASS_NAME, "error-message")`                 |
| By tag name      | `(By.TAG_NAME, "h1")`                              |

---

## Dropdown (Select element)

```python
from selenium.webdriver.support.ui import Select

def select_country(self, country: str) -> "Self":
    element = self.driver.find_element(*self._COUNTRY_DROPDOWN)
    Select(element).select_by_visible_text(country)
    return self
```

---

## Worked example — Login page

```python
from selenium.webdriver.common.by import By
from .base_page import BasePage


class LoginPage(BasePage):

    _EMAIL_INPUT       = (By.ID, "email")
    _PASSWORD_INPUT    = (By.ID, "password")
    _LOGIN_BUTTON      = (By.CSS_SELECTOR, "button[type='submit']")
    _ERROR_BANNER      = (By.CSS_SELECTOR, ".auth-error")
    _FORGOT_PWD_LINK   = (By.LINK_TEXT, "Forgot your password?")

    def enter_email(self, email: str) -> "LoginPage":
        self._type(self._EMAIL_INPUT, email)
        return self

    def enter_password(self, password: str) -> "LoginPage":
        self._type(self._PASSWORD_INPUT, password)
        return self

    def click_login(self) -> "DashboardPage":
        self._click_when_ready(self._LOGIN_BUTTON)
        from .dashboard_page import DashboardPage
        return DashboardPage(self.driver)

    def click_login_expecting_failure(self) -> "LoginPage":
        self._click_when_ready(self._LOGIN_BUTTON)
        return self

    def click_forgot_password(self) -> "ForgotPasswordPage":
        self._click_when_ready(self._FORGOT_PWD_LINK)
        from .forgot_password_page import ForgotPasswordPage
        return ForgotPasswordPage(self.driver)

    def get_error_message(self) -> str:
        return self._get_text(self._ERROR_BANNER)

    def is_error_displayed(self) -> bool:
        return self._is_displayed(self._ERROR_BANNER)
```

**Example test:**
```python
def test_login_with_valid_credentials(driver):
    dashboard = (
        LoginPage(driver)
        .enter_email("user@example.com")
        .enter_password("secret123")
        .click_login()
    )
    assert dashboard.is_welcome_message_visible()
```
