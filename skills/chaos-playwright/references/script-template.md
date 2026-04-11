# Interaction Script Template

Use this template for every Interaction Script in the Chaos Playbook. The first-person
motivation on each step is the most important part — it's what makes this useful.

---

```markdown
## [PERSONA NAME] — [Feature Name]

> *"[Tagline — the persona's voice in one sentence, specific to this feature]"*

**Why this persona will break this feature:**
[One sentence connecting this persona's psychology to a specific vulnerability in this feature.
E.g., "The Tab Hoarder's multi-hour absence will expire the payment session token, but the
checkout wizard will let them proceed to the confirmation page before discovering the order failed."]

---

### Setup

**Where they start:** [URL / app state / page they're on]
**Session state:** [How long since login / is their session fresh or stale]
**Browser state:** [Tabs open / relevant cookies or localStorage / device type]
**Prior context:** [What they were doing before, what they want to accomplish]

---

### The Scene

**Step 1.** [Action — what they do, in plain terms]
*(Why: [Motivation — why they do this, in character. Their reasoning, however flawed.]*

**Step 2.** [Action]
*(Why: [Motivation])*

**Step 3.** [Action]
*(Why: [Motivation])*

[...continue for as many steps as the scenario requires. Aim for 5–12 steps. Too few
lacks nuance; too many loses focus. The interesting stuff usually happens in steps 4–8.]*

---

### Expected Outcome

[What the UI *should* do, based on the spec or reasonable inference. Written from the
user's perspective: "The form should submit successfully and show the confirmation page."
Or: "The app should warn them their session has expired and let them pick up where they left off."]

---

### Chaos Hypothesis

[The specific bug or failure mode this script is designed to surface. Phrased as a question
or prediction. E.g.:

"**Hypothesis:** The duplicate submit on Step 6 will create two payment authorizations.
The UI will show one confirmation, but the user's card will be charged twice. The second
charge appears as a 'pending' authorization that may or may not reverse automatically."

Or:

"**Hypothesis:** When the user hits Back on Step 8 (after payment was submitted), the form
will re-render with empty fields. The user will think the payment failed and re-submit,
creating a duplicate order."

Make it specific. Make it sting. This is the "why it matters."]

---

### Automation Notes

**Automatable:** [Yes / Partially / Manual only]

[If yes or partially:]
Key automation steps:
- [Step N]: `[pseudocode or Playwright snippet]`
- [Step N]: `[what needs to be mocked or simulated — e.g., network delay, session expiry]`

[If manual only:]
Reason: [Why this scenario is hard to automate — e.g., "requires real session expiry timing",
"depends on clipboard contents from an external source", "needs device rotation simulation"]

Manual test note: [What a manual tester should specifically watch for]
```

---

## Example: The Rage Clicker × Checkout Flow

```markdown
## THE RAGE CLICKER — Checkout Flow

> *"The 'Place Order' button did nothing. I'll click it until it listens."*

**Why this persona will break this feature:**
The checkout's "Place Order" button doesn't disable fast enough after the first click,
allowing a second click at ~400ms to trigger a second payment authorization before the
first response returns.

---

### Setup

**Where they start:** `/checkout/payment` — credit card form filled, ready to submit
**Session state:** Active session, 20 minutes old
**Browser state:** Single tab, desktop Chrome
**Prior context:** Has been shopping for 10 minutes, found what they want, impatient
to be done

---

### The Scene

**Step 1.** I fill in my credit card number, expiry, and CVV.
*(Why: I'm being efficient — I type fast and I'm almost done.)*

**Step 2.** I click "Place Order" before the page has finished whatever it was doing
(a loading indicator was briefly visible on the shipping section).
*(Why: The page looked ready to me. I don't wait for spinners.)*

**Step 3.** Nothing visible happens for about 300ms.
*(Why I act: That's too long. Nothing is happening.)*

**Step 4.** I click "Place Order" again.
*(Why: My first click clearly didn't register. The button doesn't look different.)*

**Step 5.** A loading spinner appears on the button.
*(My reaction: Finally. But I already clicked twice.)*

**Step 6.** The confirmation page appears: "Order #1042 placed successfully!"
*(My reaction: Great. Done.)*

**Step 7.** I close the tab.

---

### Expected Outcome

One order is created. One payment authorization is made. The user sees one confirmation
for one order.

---

### Chaos Hypothesis

**Hypothesis:** Two payment authorizations are submitted — one per click. The UI shows
the first confirmation (Order #1042), but a second authorization for the same amount is
created in Stripe before the idempotency check can prevent it. The user's card shows two
"pending" charges. One may eventually reverse; one won't. The user calls support convinced
they were double-charged.

---

### Automation Notes

**Automatable:** Partially

Key automation steps:
- Step 2–4: `await page.click('#place-order'); await page.click('#place-order', { delay: 350 });`
  (two clicks with 350ms gap before button disables)
- Assert: Check payment processor mock for number of authorization calls
- Assert: Check database for number of orders created with same cart ID

Manual note: Monitor network tab for duplicate POST requests to `/api/orders`. Two
requests within 500ms of each other is the smoking gun.
```