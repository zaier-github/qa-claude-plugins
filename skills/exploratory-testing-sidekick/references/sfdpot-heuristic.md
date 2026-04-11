# SFDPOT Heuristic Guide
## A Framework for Exploratory Testing

SFDPOT (pronounced "sf-dee-pot") was developed by James Bach. Each letter is a *category of things to think about* when testing a feature. The goal is to prevent "happy path" tunnel vision by systematically asking: "What else could affect this?"

---

## S — Structure

**What is this feature made of?**

Structure covers the static elements — the building blocks you can see and touch.

Ask yourself:
- What UI elements exist? (buttons, forms, tables, modals, icons, tooltips)
- What configuration options exist? (settings, toggles, feature flags)
- What are the relationships between elements? (parent/child, one-to-many)
- What does the data model look like? (required fields, optional fields, data types)

**Test ideas that come from Structure thinking:**
- Test every button and interactive element — what does each one do?
- Test each configuration combination — does the feature behave correctly in all settings?
- Test with the minimum required fields vs. all optional fields filled
- Test what happens when structural elements are hidden, disabled, or removed (e.g., field not rendered)

---

## F — Function

**What does this feature do?**

Function covers the dynamic behaviors — actions, calculations, transformations, decisions.

Ask yourself:
- What are all the things this feature can do?
- What triggers each behavior? (events, user actions, system events)
- What calculations happen? (totals, scores, counts, transformations)
- What decisions does it make? (if X then Y)
- What integrations or side effects occur? (email sent, record created, webhook fired)

**Test ideas that come from Function thinking:**
- Test each function independently (not just as part of a flow)
- Test all branches of a decision: what if condition A is true? False? Both? Neither?
- Test calculations with known inputs and verify the output math
- Test that side effects happen (and only once — not duplicated)
- Test that the right function fires at the right time

---

## D — Data

**What data goes in and comes out?**

Data is the richest area for finding bugs. Most bugs live at the boundaries of what data is accepted.

Ask yourself:
- What are the valid values for each input?
- What are the *invalid* values? What *should* be rejected?
- What are the boundary values? (min, max, exactly at the limit, one over)
- What about missing data? (empty, null, not present)
- What about malformed data? (wrong type, wrong format, truncated)
- What encoding issues could arise? (unicode, special characters, whitespace)

**Test ideas that come from Data thinking:**
- Test the minimum valid value, the maximum valid value, one below min, one above max
- Test with empty/blank values in every input
- Test with Unicode characters (accents, emoji, RTL text)
- Test with data that looks like code (`<script>`, SQL, `{{template}}`)
- Test with very long strings (near and at the field limit)
- Test with numbers where strings are expected and vice versa

**The RCRCRC sub-heuristic for data states:**
- **R**eal — actual data from production (anonymized)
- **C**redible — made-up but realistic
- **R**andom — any old garbage
- **C**onfidential — data requiring special access (tests permissions)
- **R**obust — designed to stress the system
- **C**orrupt — intentionally broken/malformed

---

## P — Platform

**What environment does this run in?**

Platform covers the execution environment — every place the feature might behave differently.

Ask yourself:
- Which browsers? (Chrome, Firefox, Safari, Edge — and their mobile versions)
- Which operating systems? (Windows, macOS, iOS, Android)
- Which screen sizes? (phone portrait, phone landscape, tablet, desktop, ultra-wide)
- Which network conditions? (fast fiber, slow 3G, offline, flaky/intermittent)
- Which device capabilities? (touch vs. mouse, keyboard vs. no keyboard, dark mode)
- Which integrations or dependencies? (CDN availability, third-party services)

**Test ideas that come from Platform thinking:**
- Test on the two most different browsers your users use
- Test at a very small screen size (320px) and a very large one (2560px)
- Test with network throttling enabled (DevTools → Network → Slow 3G)
- Test on an actual mobile device, not just a browser emulator
- Test with JavaScript disabled or partially blocked

---

## O — Operations

**How do users actually use this?**

Operations covers real-world usage patterns — the messy, non-linear ways humans actually interact with software.

Ask yourself:
- What's the most common workflow? (the "happy path")
- What are the alternative paths? (start in the middle, skip a step)
- What happens if interrupted? (close tab mid-flow, go back, refresh)
- What happens with concurrent use? (two users editing the same thing)
- What happens when used repeatedly? (create 100 items, run the feature 50 times)
- What happens when combined with other features?

**Test ideas that come from Operations thinking:**
- Use the browser back button in the middle of a multi-step flow
- Refresh the page mid-workflow — does state persist correctly?
- Open the same record in two tabs and edit in both
- Perform an action very rapidly (double-click, submit multiple times)
- Complete the workflow out of the expected order (if possible)
- Use the feature as a new user with no existing data

---

## T — Time

**How does time affect this feature?**

Time is the sneakiest category — time-related bugs are often the hardest to reproduce.

Ask yourself:
- Does anything expire? (sessions, tokens, offers, invitations)
- Does anything have a timeout? (requests, locks, idle sessions)
- Does sequence matter? (does A have to happen before B?)
- Does anything depend on the current date/time? (scheduling, deadlines, age calculations)
- Does anything depend on time zones? (user's local time vs. server time)
- Does anything run on a schedule? (cron jobs, daily reports, reminder emails)

**Test ideas that come from Time thinking:**
- Test behavior when a session token is expired
- Test what happens if you leave a form open for a long time and then submit
- Test date-sensitive features with dates at boundaries (end of month, end of year, leap day)
- Test with users in different time zones (especially UTC-12 and UTC+14)
- Test scheduled features at the boundary of their trigger time
- Test what happens if two time-sensitive events happen simultaneously

---

## Putting it all together

For any feature, a complete SFDPOT sweep takes 15–30 minutes of thinking. You don't have to test everything — the goal is to think widely first, then decide what's most risky to test.

**Quick SFDPOT prompts:**
- **S**: "What's this made of?"
- **F**: "What does it do?"
- **D**: "What data does it eat?"
- **P**: "Where does it run?"
- **O**: "How will people really use it?"
- **T**: "What breaks over time?"