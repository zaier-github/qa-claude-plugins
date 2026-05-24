---
name: pom-generator
description: >
  Generates Page Object Model (POM) classes from a web page — given a URL or
  source code (HTML, React, Angular, Vue, plain JS, etc.), produces a
  ready-to-use POM class for a test automation framework. Use this skill
  whenever the user wants to create a Page Object, generate POM code, scaffold
  test page abstractions, automate interactions with a web page, or says things
  like "generate a page object for", "create a POM for this page", "make a
  page class for Playwright/Selenium/Cypress", "help me write test automation
  for this UI", "turn this page into a page object", or "I need a POM for my
  login/checkout/dashboard page". Supports all valid combinations of Java,
  JavaScript, TypeScript, and Python with Selenium, Playwright, and Cypress.
  Always trigger this skill when a URL or UI code is shared alongside any
  mention of test automation, page objects, or test frameworks.
---

# POM Generator

You generate Page Object Models — the test automation pattern that wraps a web
page's elements and interactions into a clean, reusable class. The goal is to
separate *how to find elements* from *what tests do with them*, making tests
more readable, maintainable, and resilient to UI changes.

---

## Step 1: Gather inputs

Ask for any missing information in a **single message** — don't ask one
question at a time.

### 1. The page to model

The user will provide one of:
- **A URL** — navigate to the page and extract its structure (see Step 2)
- **Source code** — HTML, React/JSX, Angular, Vue, or plain JS/TS component
- **A file path** — read it before proceeding
- **A description** — infer elements from it, but ask for code or a URL when
  possible for higher-fidelity output

### 2. Language and framework

Ask which language and test framework combination to target. Valid options:

| Language   | Selenium | Playwright | Cypress |
|------------|----------|------------|---------|
| Java       | ✅        | ✅          | ❌       |
| JavaScript | ✅        | ✅          | ✅       |
| TypeScript | ✅        | ✅          | ✅       |
| Python     | ✅        | ✅          | ❌       |

If the user picks an invalid combination (Java+Cypress or Python+Cypress),
explain that Cypress is a JavaScript/TypeScript-only framework and suggest
alternatives (e.g., Java+Playwright or Python+Playwright).

### 3. Selector strategy

Ask which locator approach to prefer:

| Strategy                 | When it works best                                       |
|--------------------------|----------------------------------------------------------|
| Semantic / role-based    | Modern accessible apps; Playwright's recommended default |
| data-testid / data-cy    | Teams that add test attributes; most stable long-term    |
| CSS selectors            | When test IDs are absent but DOM is stable               |
| XPath                    | Legacy apps, complex traversal, or dynamic IDs           |
| Mixed (auto-select best) | Skill picks the best available locator per element       |

Default to **mixed** if the user has no preference.

### 4. Optional settings (ask only if not obvious from context)

- **Class name** — defaults to the page name inferred from the URL path or
  component filename, suffixed with `Page` (e.g., `LoginPage`, `CheckoutPage`)
- **Base page class** — offer to generate a shared `BasePage` with common
  helpers (driver/page init, smart waits); useful when building multiple POMs
- **Output location** — where to save the file(s); default to current directory

---

## Step 2: Analyze the page

### If given a URL

Try in order until one succeeds:

1. **playwright-cli skill** — invoke with the URL to get a full accessibility
   snapshot. Captures JS-rendered content (React, Angular, Vue) and structured
   element data.
2. **Playwright MCP** — if available, use `browser_navigate` + `browser_snapshot`
   directly.
3. **WebFetch** — fetch raw HTML as a fallback. Remind the user that dynamically
   rendered content may be missing.

### If given source code

Read the file or snippet directly. For component code (React/Angular/Vue),
focus on the rendered template/JSX — not lifecycle methods or business logic.

### What to extract

Map the page into these categories (include only what's present):

| Category              | Examples                                                   |
|-----------------------|------------------------------------------------------------|
| Inputs                | text, password, email, search, textarea                    |
| Buttons and actions   | submit, cancel, confirm, CTA, icon buttons                 |
| Navigation            | nav links, tabs, breadcrumbs, pagination, back/next        |
| Selectors and pickers | dropdowns, checkboxes, radios, date pickers, toggles       |
| Lists and tables      | data tables, list items, row actions                       |
| Feedback elements     | error messages, success banners, loaders, toast alerts     |
| Forms                 | group inputs under their form context                      |
| Modals and overlays   | dialogs, popovers, side drawers                            |
| Page identity         | main heading, page title, unique identifiers               |

For each element, determine:
- A **descriptive name** based on what it *does*, not what it *is*
  (e.g., `loginButton` not `button1`, `emailInput` not `field2`)
- The **best locator** given the user's chosen strategy
- The **interaction type** (click, type, select, check, assert text, etc.)

---

## Step 3: Generate the POM

Read `references/<language>-<framework>.md` before writing any code — it
contains the exact class template, element patterns, and a worked example.

**Reference file index:**
- `references/java-selenium.md`
- `references/java-playwright.md`
- `references/javascript-selenium.md`
- `references/javascript-playwright.md`
- `references/javascript-cypress.md`
- `references/typescript-selenium.md`
- `references/typescript-playwright.md`
- `references/typescript-cypress.md`
- `references/python-selenium.md`
- `references/python-playwright.md`

### Universal POM principles

These apply regardless of language or framework:

- **One class per page or major component** — don't mix multiple pages into one
- **Locators as fields/properties, interactions as methods** — the test reads
  `loginPage.clickSubmit()`, not `driver.findElement(...).click()`
- **Action methods return the page object** where it makes sense, enabling
  fluent chaining: `loginPage.enterEmail(e).enterPassword(p).clickLogin()`
- **Verification helpers expose state without asserting** — `isLoggedIn()`,
  `getErrorMessage()`, `isSubmitEnabled()`. Tests make assertions; POMs surface
  data
- **No test assertions inside the POM** — keep the POM ignorant of test logic
- **Named after the user action, not the DOM** — `clickAddToCart()` not
  `clickButton3()`

### Naming conventions

Apply language idioms:
- **Java/JS/TS**: `camelCase` for methods and fields, `PascalCase` for class
- **Python**: `snake_case` for methods and properties, `PascalCase` for class
- **Class name**: `<PageName>Page` (e.g., `LoginPage`, `DashboardPage`)

---

## Step 4: Deliver

1. Show the generated POM code inline in the conversation
2. Save to the requested output location (ask if not specified; default to CWD)
3. If a base page class was requested, generate it as a separate file
4. Provide a brief summary:
   - What page was modeled
   - Elements extracted (count and categories)
   - Selector strategy used
   - A short example showing the POM used in a real test (5–10 lines)

---

## Subagents (large pages only)

For pages with 4+ distinct sections each containing 5+ elements (e.g., a
dashboard with header, sidebar, data table, and footer), consider splitting
into multiple POMs — one per section — and generating them in parallel.

Ask the user first: "This page is large. Would you like one combined POM, or
one class per section (header, sidebar, etc.)?"

If they choose per-section, spawn one subagent per section with:
- The section's elements
- The chosen language/framework
- The output path

For most pages, generate inline without subagents.
