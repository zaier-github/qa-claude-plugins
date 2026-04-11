# Persona Library

Full profiles for the Chaos Playwright company. Each profile includes: psychology (the *why*),
signature behaviors (the *what*), and what they reliably break (the *target*).

Use these profiles to write authentic first-person motivation in Interaction Scripts.

---

## Table of Contents
- [Core Company](#core-company)
  - [The Rage Clicker](#the-rage-clicker)
  - [The Tab Hoarder](#the-tab-hoarder)
  - [The Copy-Paster](#the-copy-paster)
  - [The Back-Button Abuser](#the-back-button-abuser)
  - [The Form Spammer](#the-form-spammer)
  - [The Accidental Tourist](#the-accidental-tourist)
  - [The Mobile Fumbler](#the-mobile-fumbler)
  - [The Slow Typist](#the-slow-typist)
- [Specialist Company](#specialist-company)
  - [The Permission Paranoid](#the-permission-paranoid)
  - [The Data Hoarder](#the-data-hoarder)
  - [The Parallel Operator](#the-parallel-operator)
  - [The Keyboard Warrior](#the-keyboard-warrior)
  - [The International](#the-international)
  - [The Slow Connection](#the-slow-connection)

---

## Core Company

### The Rage Clicker

**Tagline:** *"I clicked it. Why isn't it doing anything. I'll click it again."*

**Psychology:** Grew up on desktop software that responded instantly. Interprets latency
as non-response. Has zero patience for loading states. Believes clicking more times will
help. Not malicious — just fast and frustrated. Treats your UI as a vending machine that
owes them an immediate result.

**Signature behaviors:**
- Double- and triple-clicks every interactive element
- Clicks "Submit" immediately, then again at 300ms, then again at 800ms
- Clicks disabled or visually inactive buttons repeatedly
- Clicks "Cancel" on a loading spinner, then immediately tries to re-start the operation
- Rage-clicks form fields that are loading, dropdowns that are animating, tabs mid-transition
- Clicks "Confirm" on a modal before reading it

**What they reliably break:**
- Duplicate form submissions (two orders, two payments, two accounts)
- Race conditions between click handlers
- UI state that doesn't disable buttons fast enough after first click
- Optimistic UI updates that conflict when the same operation is triggered twice
- Payment flows without idempotency keys
- Any "are you sure?" dialog that can be double-confirmed

**In their own voice:**
> "I click the button, nothing happens. I click it again. Still loading. One more time.
> I don't have all day for this."

---

### The Tab Hoarder

**Tagline:** *"I started this checkout three hours ago, I'll finish it now."*

**Psychology:** Multitasker. Always has 20+ tabs open across multiple windows. Starts flows
on their lunch break, returns to them after a meeting. Considers the browser their
external memory. Assumes apps preserve state indefinitely. Gets genuinely confused and
frustrated when their "saved" work is gone.

**Signature behaviors:**
- Returns to a flow after 2–8 hours away
- Opens the same app in multiple tabs without realizing it
- Opens a "complete your profile" email link in a new tab while still on the app in another
- Bookmarks mid-flow pages and returns to them days later
- Has your app's home page open in Tab 1 and a deep-linked feature in Tab 7

**What they reliably break:**
- Session expiry without graceful state recovery ("your session has expired" right before checkout)
- CSRF token invalidation after long idle periods
- Forms that lose state on session refresh
- Deep-link behavior when the user isn't authenticated or is authenticated as a different user
- Optimistic UI that goes stale when returned to after background refresh
- "One-time" flow pages (email verification links, payment redirects) visited after delay

**In their own voice:**
> "I was right in the middle of the checkout but I had to take a call. I'm back now.
> What do you mean my cart is empty? I had $200 of stuff in there."

---

### The Copy-Paster

**Tagline:** *"I never type if I can paste."*

**Psychology:** Efficiency-maximizer. Has all their important data — names, addresses, codes,
IDs — in documents, spreadsheets, emails, and Slack. Typing feels wasteful when it's already
written somewhere. Assumes pasting is equivalent to typing. Completely unaware of invisible
characters, encoding differences, or formatting artifacts that come along for the ride.

**Signature behaviors:**
- Pastes full name from email signature (includes title, company, line breaks)
- Pastes address from a Google Maps result (includes map link text)
- Pastes phone number from a contact card (includes country code, parentheses, dashes)
- Pastes dates from spreadsheets (various locale formats, sometimes with time components)
- Pastes coupon codes from emails (may include surrounding whitespace or HTML entities)
- Pastes passwords from a password manager that adds a space after
- Pastes from a PDF (non-breaking spaces, ligatures, smart quotes instead of straight quotes)

**What they reliably break:**
- Phone number validation (can't handle +1 (555) 123-4567)
- Name fields with length limits (full signature block overflows)
- Date pickers that expect a specific format (MM/DD vs DD/MM vs YYYY-MM-DD)
- Email validation (smart quotes from Word render the @ sign differently)
- Coupon/promo code fields (trailing space means "SAVE20 " doesn't match "SAVE20")
- Password confirmation fields (pasted password with extra space doesn't match)
- Any field that processes input character-by-character (some autocomplete implementations)

**In their own voice:**
> "My address is already in my spreadsheet so I just highlighted and pasted.
> Why does it say the ZIP code is invalid? I copy-pasted it straight from the USPS site."

---

### The Back-Button Abuser

**Tagline:** *"Back means back. I don't care what your wizard says."*

**Psychology:** The browser back button is the universal "undo" for the web. They learned
this in 2003 and it's been true their whole internet life. They don't understand (and don't
care) that your multi-step flow has assumptions about forward-only navigation. Back is escape.
Back is their safety net. They use it constantly and expect the world to be coherent afterwards.

**Signature behaviors:**
- Hits back on the confirmation/success page ("wait, did that actually go through?")
- Hits back mid-wizard, changes something, goes forward again (expects the later steps to update)
- Hits back after submitting a form while it was processing
- Hits back multiple times past the start of a flow, landing outside your app
- Uses back to "cancel" an action instead of clicking a Cancel button
- Bookmarks the confirmation page URL and navigates to it later

**What they reliably break:**
- Checkout wizards that don't handle back navigation (step 3 showing step 2's data)
- Payment flows where going back after submission causes a duplicate charge
- Forms that re-submit on back navigation (especially POST-without-redirect)
- Success pages that show stale/empty state when revisited
- Token-gated URLs (email verification, payment redirect) that can only be used once
- Browser history states that leak sensitive data (order details in URL)
- "Are you sure you want to leave?" guards that fire unnecessarily

**In their own voice:**
> "I hit back to check my shipping address and now it's asking me to enter my credit
> card again. I already paid. Did my order go through or not?"

---

### The Form Spammer

**Tagline:** *"Enter submits. That's how forms work."*

**Psychology:** Impatient and keyboard-native. Learned that Enter = Submit in every program
they've ever used. Doesn't scroll forms to check for missed fields. Expects immediate feedback.
Hits submit constantly during "processing" states because silence means failure to them.
Not trying to break anything — just moving fast.

**Signature behaviors:**
- Hits Enter to submit a form after filling the first required field (leaving others empty)
- Presses Enter while still in the email field, triggering submission before filling password
- Clicks Submit while autocomplete dropdown is still showing (autocomplete selection + submit)
- Refreshes the page when the submit button goes into a loading state
- Submits the same form from two browser tabs simultaneously
- Hits Enter on a search field before finishing typing
- Clicks "Place Order" while the payment method is still loading/validating

**What they reliably break:**
- Forms with progressive validation that fires before all fields are filled
- Autocomplete + submit race conditions (email autocomplete selects wrong address at submit)
- Duplicate submission on double-Enter
- Loading states that don't block re-submission
- Multi-step forms that advance to step 2 with incomplete step 1 data
- Search that fires on every keystroke AND on Enter (triggers two requests, shows two results)

**In their own voice:**
> "I filled in my email and hit Enter. It said 'password is required.' What password?
> I didn't get to the password field yet."

---

### The Accidental Tourist

**Tagline:** *"How did I get here? How do I get out?"*

**Psychology:** Arrived somewhere unexpected — clicked the wrong link in an email, was
redirected to an unfamiliar page, landed on a deep URL without context. Doesn't understand
the app's navigation model. Tries to escape in every wrong direction. Their confusion is
genuine and their click targets are unpredictable. They represent every user who's ever
ended up somewhere they didn't mean to go.

**Signature behaviors:**
- Clicks the logo to go "home" mid-flow (abandoning unsaved state)
- Closes modals by clicking the backdrop (sometimes intentionally, sometimes not)
- Uses the browser's "find on page" to navigate instead of the app's search
- Clicks every link in a confirmation email, multiple times
- Opens support chat to ask "what is this screen?" mid-checkout
- Tries to navigate to an account settings page while in an embedded iframe flow
- Scrolls to the bottom looking for a "cancel" or "back" button that isn't there

**What they reliably break:**
- Flows that have no visible escape route (users feel trapped → support tickets)
- Modal-heavy UIs where backdrop clicks destroy progress without confirmation
- Logo/home links that navigate away from critical flows without warning
- Emails with multiple CTAs where clicking any of them creates duplicate flows
- Embedded flows (iframes, OAuth popups) where navigation outside the frame breaks state

**In their own voice:**
> "I clicked the logo to go to the homepage and now I can't find where I was.
> I was in the middle of something important."

---

### The Mobile Fumbler

**Tagline:** *"I'm trying to tap the right thing, I promise."*

**Psychology:** On their phone, in a hurry, probably outdoors. Small screen, variable
connection, fat thumbs relative to tap targets. Their world is full of interruptions —
phone calls, notifications, switching apps. They put your app in the background and return
to find it has reset. They rotate their phone mid-flow. They type with one thumb while
holding a coffee.

**Signature behaviors:**
- Taps adjacent elements (misses a small button, hits the link behind it)
- Rotates device mid-form (triggers layout recalculation, sometimes resets form state)
- Receives a phone call mid-checkout, returns to find app has reloaded
- Switches to a different app to check an email, comes back to a session timeout
- Uses predictive text that replaces their carefully typed input
- Pinches to zoom on a non-zoomable page, interacts with misaligned elements
- Zooms in on a form field, can't see the submit button anymore

**What they reliably break:**
- Touch targets that are technically 44px but practically harder to hit in context
- Orientation change handling (form data lost on rotation, layout broken in landscape)
- Background-to-foreground state recovery (app assumes it was never backgrounded)
- Fixed-position elements that interfere with keyboard (submit button hidden behind keyboard)
- Forms where the mobile keyboard covers the active field
- Any flow longer than 3 steps (attention span + interruptions = abandonment)

**In their own voice:**
> "I was almost done with the payment and my mom called. When I came back it had
> logged me out and my cart was empty."

---

### The Slow Typist

**Tagline:** *"I'm getting there, stop rushing me."*

**Psychology:** Two-finger typist. Maybe elderly, maybe just careful and methodical. Types
slowly and deliberately. Reads every label before filling it. By the time they're done with
a long form, your session token has expired, your auto-save has fired 40 times, your
real-time validation has shown and hidden error messages in a distracting loop.

**Signature behaviors:**
- Takes 15+ minutes to complete a multi-field form
- Pauses for 30+ seconds between fields (validation fires on blur, then fires again on focus)
- Types in bursts of 2–3 characters with 5-second pauses
- Re-reads the entire form before hitting submit
- Hits the tab key to move between fields, triggering validation on each field they leave
- Has the form timing out during completion on networks that expire idle connections

**What they reliably break:**
- Session timeouts during form completion (especially for longer flows)
- Real-time validation that fires too eagerly (showing "invalid email" mid-keystroke)
- Auto-save that fires so frequently it creates race conditions with manual save
- CSRF tokens that expire before form submission
- File upload timeouts (uploading a large file on a slow connection within the idle timeout)
- Password strength meters that distract and slow them further

**In their own voice:**
> "I was filling out the form and when I went to submit it said my session had expired.
> I had to start all over. All that work, gone."

---

## Specialist Company

### The Permission Paranoid

**Psychology:** Has read too many privacy articles. Denies every permission request without
reading it. Camera, microphone, location, notifications, clipboard — all denied reflexively.
Then interacts with your app as if they said yes.

**What they break:** ID verification flows, geolocation features, push notifications,
clipboard-dependent paste flows, camera-based uploads. Any flow that silently fails when
a permission is denied (vs. gracefully degrading).

---

### The Data Hoarder

**Psychology:** Power user who's been with your platform for years. Has 10,000 records,
500 tags, a history that predates your current schema, and edge-case data created during
your beta that never should have existed.

**What they break:** Pagination (doesn't test with 3 items), dropdowns that load all options,
search with huge result sets, export features with large datasets, bulk operations, any
feature that assumed "most users have < 50 of these."

---

### The Parallel Operator

**Psychology:** Productivity maximalist. Has your app open in 3 browser windows. Makes
changes in window 1, then tries to do something in window 3 that depends on the state
from window 1. Assumes everything is synchronized in real time.

**What they break:** Optimistic UI updates that conflict across tabs, concurrent edit
conflicts, checkout flows where a coupon is applied in two tabs simultaneously, any state
that's stored client-side (localStorage, cookies) and modified in one tab then read in another.

---

### The Keyboard Warrior

**Psychology:** Accessibility power user, or just someone who finds the mouse slow. Lives
on Tab, Enter, Escape, arrow keys. Discovers every focus trap, every non-focusable element,
every keyboard shortcut conflict.

**What they break:** Custom dropdown components that aren't keyboard navigable, modals
without focus trapping, forms without logical tab order, buttons that only respond to click
(not Enter/Space), tooltips that only appear on hover.

---

### The International

**Psychology:** Using your app from outside your assumed locale. Their name has accents or
non-Latin characters. Their date format is DD/MM/YYYY. Their decimal separator is a comma.
Their phone number format is different. Their timezone is UTC+5:30.

**What they break:** Name fields that reject non-ASCII, date pickers that assume MM/DD/YYYY,
phone validation that doesn't accept international formats, prices displayed without currency
context, timezone-naive date handling ("order placed on Jan 3" — which timezone?).

---

### The Slow Connection

**Psychology:** Rural user, international traveler, mobile on a crowded network.
Their connection drops mid-operation. Requests time out. They see spinners for 30+ seconds.
They click the submit button twice because nothing happened after 10 seconds.

**What they break:** Upload timeouts, duplicate submissions from double-clicks on slow
responses, optimistic UI that shows success before server confirmation (then rolls back),
any operation that isn't resumable after interruption, file uploads without progress indication.