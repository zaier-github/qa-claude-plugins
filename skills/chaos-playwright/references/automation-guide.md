# Automation Guide

How to translate Chaos Playwright Interaction Scripts into executable test code.
Not every scenario is automatable — this guide helps you decide what to automate
and how to implement the tricky parts.

---

## Automation decision matrix

| Scenario type | Automatable? | Notes |
|--------------|-------------|-------|
| Double-click / rapid re-click | ✅ Yes | `page.click()` twice with delay |
| Session expiry | ✅ Yes | Manipulate cookie expiry or mock time |
| Back button navigation | ✅ Yes | `page.goBack()` |
| Form submission timing | ✅ Yes | Intercept requests, add delay |
| Paste with special characters | ✅ Yes | `page.fill()` with special chars |
| Concurrent tabs / parallel ops | ✅ Yes | Multiple browser contexts |
| Network interruption | ✅ Yes | `page.route()` to simulate failures |
| Device rotation | ✅ Partially | `page.setViewportSize()`, but not real rotation |
| Phone call interruption | ❌ Manual | Can only simulate by backgrounding via script |
| Clipboard from external app | ✅ Partially | Inject content directly; can't simulate source |
| Real session timeout timing | ✅ Yes | Mock clock or set short expiry |
| PDF paste artifacts | ✅ Partially | Inject known PDF-paste strings directly |

---

## Playwright recipes

### Rage Clicker — rapid double-submit

```typescript
// Two clicks with 350ms gap (before button likely disables)
await page.click('#submit-button');
await page.waitForTimeout(350);
await page.click('#submit-button');

// Assert only one request was made
const requests: string[] = [];
page.on('request', req => {
  if (req.url().includes('/api/orders')) requests.push(req.url());
});
// ... trigger scenario ...
expect(requests.length).toBe(1); // fails if double-submit went through
```

### Tab Hoarder — simulate session expiry

```typescript
// Method 1: Delete session cookie
await page.context().clearCookies();

// Method 2: Set cookie with past expiry
await page.context().addCookies([{
  name: 'session',
  value: 'expired-token',
  domain: 'localhost',
  expires: Math.floor(Date.now() / 1000) - 3600, // 1 hour ago
}]);

// Method 3: Intercept auth endpoint to return 401
await page.route('**/api/**', route => {
  route.fulfill({ status: 401, body: '{"error": "session expired"}' });
});
```

### Back-Button Abuser — back after form submit

```typescript
// Submit form
await page.click('#submit-button');
await page.waitForURL('**/confirmation');

// Immediately go back
await page.goBack();

// Verify: is the form re-shown? Does it re-submit on load?
await expect(page).toHaveURL(/checkout/);

// Check for duplicate submissions in network requests
const postRequests = requests.filter(r => r.method === 'POST');
expect(postRequests.length).toBe(1); // should not have re-submitted
```

### Copy-Paster — inject clipboard artifacts

```typescript
// Paste name with email signature artifacts
await page.fill('#full-name', 'Jane Smith\nSr. Product Manager\nAcme Corp');

// Paste phone with formatting
await page.fill('#phone', '+1 (555) 123-4567');

// Paste email with trailing space (common from copy from text)
await page.fill('#email', 'user@example.com ');

// Paste coupon code with zero-width space (common in email clients)
await page.fill('#coupon', 'SAVE20\u200B');

// Paste content with smart quotes (from Word/Google Docs)
await page.fill('#address', '\u201C123 Main St\u201D'); // "123 Main St"
```

### Form Spammer — submit before all fields filled

```typescript
// Fill only first field, then submit
await page.fill('#email', 'user@example.com');
await page.keyboard.press('Enter'); // submits via Enter key

// Check: does the form validate properly or advance with incomplete data?
await expect(page.locator('.error-message')).toBeVisible();
await expect(page.locator('#password')).toBeFocused(); // focus should move to missing field
```

### Slow Connection — simulate network delay and timeout

```typescript
// Add latency to all API calls
await page.route('**/api/**', async route => {
  await new Promise(resolve => setTimeout(resolve, 5000)); // 5 second delay
  await route.continue();
});

// Simulate request failure (timeout behavior)
await page.route('**/api/payment**', route => {
  route.abort('timedout');
});

// Simulate partial failure (connection dropped mid-response)
await page.route('**/api/upload**', async route => {
  await route.fulfill({
    status: 200,
    body: '{"partial": true}', // incomplete response
  });
});
```

### Parallel Operator — concurrent operations in two tabs

```typescript
// Open two pages in the same browser context (shared session)
const page1 = await context.newPage();
const page2 = await context.newPage();

await page1.goto('/settings');
await page2.goto('/settings');

// Make conflicting changes simultaneously
await Promise.all([
  page1.fill('#display-name', 'Name from Tab 1'),
  page2.fill('#display-name', 'Name from Tab 2'),
]);

// Submit both
await Promise.all([
  page1.click('#save'),
  page2.click('#save'),
]);

// Check which name won (last write wins? conflict detected?)
const savedName = await page1.locator('#display-name').inputValue();
// assert specific behavior based on expected conflict resolution
```

### Mobile Fumbler — device rotation

```typescript
// Portrait
await page.setViewportSize({ width: 390, height: 844 }); // iPhone 14

// Fill part of form
await page.fill('#email', 'user@example.com');

// "Rotate" to landscape
await page.setViewportSize({ width: 844, height: 390 });

// Check: is the email field value preserved?
await expect(page.locator('#email')).toHaveValue('user@example.com');

// Check: is the submit button still visible?
await expect(page.locator('#submit')).toBeVisible();
```

---

## What to assert

The most important assertions for chaos scenarios:

```typescript
// Network request count (duplicate submission detection)
const submissionCount = requests.filter(r => r.url().includes('/api/orders')).length;
expect(submissionCount).toBe(1);

// Database state (requires API or direct DB check)
const orders = await apiClient.getOrders({ userId: 'test-user' });
expect(orders.length).toBe(1);

// Error recovery — user should be able to complete the flow
await expect(page.locator('.error-recovery')).toBeVisible();
await expect(page.locator('#retry-button')).toBeEnabled();

// State preservation — data shouldn't be lost
await expect(page.locator('#cart-item-count')).toHaveText('3');

// Graceful degradation — something is better than nothing
await expect(page.locator('.feature-unavailable')).toBeVisible(); // not a blank page
```

---

## Scenarios that need manual testing

Some Chaos Playwright scenarios can't be reliably automated:

- **Real clipboard content from external apps**: Inject the content directly; you can't
  simulate the actual copy-from-PDF experience, but you can test the pasted result.
- **Phone call interruption**: Simulate by navigating away and back, or using the app
  lifecycle events in a real device test framework (Detox, Appium).
- **Real network variability**: Charles Proxy, Network Link Conditioner, or `tc` on Linux
  give more realistic simulation than Playwright's network mocking.
- **Touch pressure / force touch**: Not simulatable in Playwright; requires real devices.

For these, write a manual test guide card that a human tester can follow. Include:
- Exact preconditions
- Step-by-step instructions
- What to watch for
- How to log/report what they find