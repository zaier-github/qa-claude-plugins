# Python + Playwright — POM Templates

## Required packages

```bash
pip install playwright
playwright install
```

---

## Base page class — Sync API

Playwright Python offers both sync and async APIs. Default to sync unless
the user's project uses async (e.g., pytest-asyncio).

```python
from playwright.sync_api import Page, Locator


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str) -> None:
        self.page.goto(url)

    def title(self) -> str:
        return self.page.title()

    def wait_for_load(self) -> None:
        self.page.wait_for_load_state("networkidle")
```

---

## POM class template (sync)

Locators in Playwright are lazy — define them as properties or methods.
Prefer semantic locators (`get_by_role`, `get_by_label`, `get_by_test_id`)
over raw CSS/XPath.

```python
from playwright.sync_api import Page, Locator
from .base_page import BasePage


class [PageName]Page(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)

    # --- Locator properties -----------------------------------------------

    @property
    def _some_input(self) -> Locator:
        return self.page.get_by_label("Field label")

    @property
    def _submit_button(self) -> Locator:
        return self.page.get_by_role("button", name="Submit")

    @property
    def _error_message(self) -> Locator:
        return self.page.locator(".error-message")

    # --- Action methods ---------------------------------------------------

    def enter_value(self, value: str) -> "[PageName]Page":
        self._some_input.fill(value)
        return self

    def click_submit(self) -> "NextPage":
        self._submit_button.click()
        from .next_page import NextPage
        return NextPage(self.page)

    # --- State / verification methods ------------------------------------

    def get_error_message(self) -> str:
        return self._error_message.text_content()

    def is_error_visible(self) -> bool:
        return self._error_message.is_visible()

    def is_submit_enabled(self) -> bool:
        return self._submit_button.is_enabled()
```

---

## Locator strategy cheatsheet

| Strategy            | Python (sync)                                       |
|---------------------|-----------------------------------------------------|
| By ARIA role        | `page.get_by_role("button", name="Submit")`         |
| By label            | `page.get_by_label("Email address")`                |
| By placeholder      | `page.get_by_placeholder("Enter email")`            |
| By test ID          | `page.get_by_test_id("submit-btn")`                 |
| By text             | `page.get_by_text("Sign in")`                       |
| By CSS              | `page.locator("button[type='submit']")`             |
| By XPath            | `page.locator("xpath=//button[@type='submit']")`    |
| Nth match           | `page.locator(".item").nth(2)`                      |
| Filter by text      | `page.locator(".row").filter(has_text="Active")`    |

---

## Interaction cheatsheet

| Interaction         | Playwright API                        |
|---------------------|---------------------------------------|
| Fill text field     | `locator.fill("value")`               |
| Click               | `locator.click()`                     |
| Check checkbox      | `locator.check()`                     |
| Uncheck checkbox    | `locator.uncheck()`                   |
| Select dropdown     | `locator.select_option("value")`      |
| Get text            | `locator.text_content()`              |
| Get input value     | `locator.input_value()`               |
| Is visible          | `locator.is_visible()`                |
| Is enabled          | `locator.is_enabled()`                |
| Wait for visible    | `locator.wait_for()`                  |
| Hover               | `locator.hover()`                     |
| Press key           | `locator.press("Enter")`              |

---

## Async variant

If the project uses `pytest-asyncio`, swap sync for async throughout:

```python
from playwright.async_api import Page, Locator


class LoginPage:
    def __init__(self, page: Page):
        self.page = page

    async def enter_email(self, email: str) -> "LoginPage":
        await self.page.get_by_label("Email").fill(email)
        return self

    async def click_login(self) -> "DashboardPage":
        await self.page.get_by_role("button", name="Log in").click()
        return DashboardPage(self.page)
```

---

## Worked example — Login page (sync)

```python
from playwright.sync_api import Page, Locator
from .base_page import BasePage


class LoginPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)

    @property
    def _email_input(self) -> Locator:
        return self.page.get_by_label("Email")

    @property
    def _password_input(self) -> Locator:
        return self.page.get_by_label("Password")

    @property
    def _login_button(self) -> Locator:
        return self.page.get_by_role("button", name="Log in")

    @property
    def _error_banner(self) -> Locator:
        return self.page.locator("[role='alert']")

    @property
    def _forgot_password_link(self) -> Locator:
        return self.page.get_by_text("Forgot your password?")

    def enter_email(self, email: str) -> "LoginPage":
        self._email_input.fill(email)
        return self

    def enter_password(self, password: str) -> "LoginPage":
        self._password_input.fill(password)
        return self

    def click_login(self) -> "DashboardPage":
        self._login_button.click()
        from .dashboard_page import DashboardPage
        return DashboardPage(self.page)

    def click_login_expecting_failure(self) -> "LoginPage":
        self._login_button.click()
        return self

    def click_forgot_password(self) -> "ForgotPasswordPage":
        self._forgot_password_link.click()
        from .forgot_password_page import ForgotPasswordPage
        return ForgotPasswordPage(self.page)

    def get_error_message(self) -> str:
        return self._error_banner.text_content()

    def is_error_visible(self) -> bool:
        return self._error_banner.is_visible()
```

**Example test:**
```python
def test_login_with_valid_credentials(page: Page):
    dashboard = (
        LoginPage(page)
        .enter_email("user@example.com")
        .enter_password("secret123")
        .click_login()
    )
    assert dashboard.is_welcome_message_visible()
```
