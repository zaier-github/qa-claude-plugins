# Domain Casting Guide

Which personas to cast for specific feature domains and flow types. Use this when the
user hasn't specified personas — cast the most relevant 3–5 for their feature.

---

## Checkout / Payment Flows

**Primary cast:**
- 🎭 **The Rage Clicker** — Duplicate payment submissions are the highest-impact failure mode
- 🎭 **The Tab Hoarder** — Session expiry mid-checkout, cart going stale
- 🎭 **The Back-Button Abuser** — Going back after payment submission, duplicate charge risk
- 🎭 **The Copy-Paster** — Card number with spaces, billing address from Google Maps

**Also consider:**
- The Slow Connection — Payment timeout, retry leading to double charge
- The Form Spammer — Submitting before payment method loads

**Scenarios to specifically look for:**
- Double authorization (Rage Clicker + any submit pattern)
- Session expiry between "enter payment" and "confirm" steps (Tab Hoarder)
- POST-without-redirect causing re-submission on back navigation (Back-Button Abuser)
- Coupon code with trailing space not matching (Copy-Paster)

---

## Registration / Sign-Up Forms

**Primary cast:**
- 🎭 **The Copy-Paster** — Email from clipboard with formatting, password from manager with trailing space
- 🎭 **The Form Spammer** — Enter key submits before all fields filled
- 🎭 **The Rage Clicker** — Double-submitting creates two accounts
- 🎭 **The International** — Non-ASCII name, international phone format

**Also consider:**
- The Slow Typist — Real-time validation fires aggressively on every keystroke
- The Back-Button Abuser — Going back from email verification step

**Scenarios to specifically look for:**
- Duplicate account creation (Rage Clicker)
- Email with invisible trailing character accepted but not deliverable (Copy-Paster)
- International phone number rejected (International)
- Password with space added by password manager doesn't match confirmation (Copy-Paster)

---

## File Upload / Media Upload

**Primary cast:**
- 🎭 **The Rage Clicker** — Uploads same file twice, or clicks Upload before previous finishes
- 🎭 **The Mobile Fumbler** — Phone call interrupts upload, file half-uploaded
- 🎭 **The Slow Connection** — Upload timeout, partial upload, resume capability
- 🎭 **The Permission Paranoid** — Camera/file access denied, app silent about why

**Also consider:**
- The Tab Hoarder — Returns to upload page after leaving during upload
- The Copy-Paster — Drags file from email client, brings unexpected metadata

**Scenarios to specifically look for:**
- Partial upload not cleaned up on timeout (Slow Connection)
- Duplicate file stored when upload button clicked twice (Rage Clicker)
- Permission denial with no graceful fallback or explanation (Permission Paranoid)
- Upload resumption after app backgrounded on mobile (Mobile Fumbler)

---

## Multi-Step Wizards / Onboarding

**Primary cast:**
- 🎭 **The Back-Button Abuser** — Goes back to earlier steps, later steps show stale data
- 🎭 **The Tab Hoarder** — Returns mid-wizard after hours, session expired
- 🎭 **The Accidental Tourist** — Gets confused, tries to escape via logo or close
- 🎭 **The Form Spammer** — Advances steps before filling required fields

**Also consider:**
- The Rage Clicker — Clicks "Next" multiple times, advances two steps
- The Slow Typist — Session timeout during a long step

**Scenarios to specifically look for:**
- Step 3 data persists when user goes back to Step 1 and changes Step 1 data (Back-Button Abuser)
- Wizard loses progress on session expiry with no recovery (Tab Hoarder)
- Advancing past required fields (Form Spammer)
- Closing a modal mid-wizard with unsaved data (Accidental Tourist)

---

## Search / Filtering / Tables

**Primary cast:**
- 🎭 **The Form Spammer** — Searches before finishing typing, gets wrong results
- 🎭 **The Data Hoarder** — 10,000 results, pagination breaks, export times out
- 🎭 **The Copy-Paster** — Pastes search term with quotes or special characters
- 🎭 **The Rage Clicker** — Clicks a filter, clicks it again before results load

**Also consider:**
- The Back-Button Abuser — Browser back from a search result clears the search
- The Keyboard Warrior — Filter dropdowns not keyboard accessible

**Scenarios to specifically look for:**
- Two simultaneous search requests racing, wrong results shown (Form Spammer + any)
- Pagination breaks at limits (Data Hoarder)
- Search injection via pasted special characters (Copy-Paster)
- Filter state lost on back navigation (Back-Button Abuser)

---

## Account / Settings / Profile

**Primary cast:**
- 🎭 **The Parallel Operator** — Same settings open in two tabs, conflicting saves
- 🎭 **The Copy-Paster** — Name, address, bio pasted from various sources
- 🎭 **The Tab Hoarder** — Settings page stale when returned to after hours
- 🎭 **The International** — Name with accents, non-standard address format

**Also consider:**
- The Back-Button Abuser — Goes back after saving, sees old data (cache not invalidated)
- The Rage Clicker — Saves settings twice, creates duplicate history

**Scenarios to specifically look for:**
- Last-write-wins conflict on concurrent edit (Parallel Operator)
- Non-ASCII characters in profile fields causing display or storage issues (International)
- Stale cache showing old data after save (Tab Hoarder + Back-Button)

---

## Authentication / Login / Session Management

**Primary cast:**
- 🎭 **The Tab Hoarder** — Session expired in background tab, discovers mid-action
- 🎭 **The Copy-Paster** — Password from manager with trailing space or smart quotes
- 🎭 **The Rage Clicker** — Multiple login attempts before first response
- 🎭 **The Back-Button Abuser** — Goes back after logout, lands on authenticated page

**Also consider:**
- The Form Spammer — Hits Enter on email field before typing password
- The Permission Paranoid — Denies cookie consent, session breaks

**Scenarios to specifically look for:**
- Cached authenticated page visible after logout (Back-Button Abuser)
- Password with trailing space (common from password managers) rejected but not explained (Copy-Paster)
- Rate limiting on login attempts (Rage Clicker triggers lockout of the real user)
- Session expiry surfaced at the worst moment — mid-checkout, mid-form (Tab Hoarder)

---

## Dashboards / Data Visualization

**Primary cast:**
- 🎭 **The Data Hoarder** — Huge datasets cause slow loads, broken charts, export failures
- 🎭 **The Parallel Operator** — Dashboard in two windows, live data diverges
- 🎭 **The Tab Hoarder** — Returns to dashboard after hours, charts show stale data
- 🎭 **The Keyboard Warrior** — Charts not keyboard navigable, no screen reader labels

**Also consider:**
- The Mobile Fumbler — Complex charts unusable on small screen
- The Slow Connection — Dashboard never finishes loading, partial data shown

---

## Mobile / Responsive Flows (any feature on mobile)

**Always add to existing cast:**
- 🎭 **The Mobile Fumbler** — Touch targets, orientation, interruptions
- 🎭 **The Slow Connection** — Mobile network reliability

**Mobile-specific scenarios to add to any playbook:**
- Device rotation mid-form (does form reset?)
- App backgrounded mid-flow (does state recover?)
- Keyboard covering submit button (can user complete the form?)
- Double-tap interpreted as zoom vs. two taps (touch event handling)