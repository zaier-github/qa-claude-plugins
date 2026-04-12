# OWASP Top 10 QA Checklist (2021 Edition)

Use this during QA to check for the most critical web application security risks.
For each item: ✅ Pass | ❌ Fail (needs fix) | ⚠️ Uncertain (needs developer review) | N/A

---

## A01: Broken Access Control

**Risk**: Users can access resources or actions they shouldn't (other users' data, admin functions).

| # | QA Check |
|---|----------|
| 1.1 | Can you access another user's data by changing a user ID in the URL? (e.g., `/users/123/orders` → try `/users/124/orders`) |
| 1.2 | Can a regular user access admin pages? (e.g., `/admin`, `/dashboard/settings`) |
| 1.3 | Can you perform actions after logging out (try accessing a URL directly)? |
| 1.4 | Are there direct object reference parameters in the URL that aren't validated? |
| 1.5 | Do API responses include more data than the UI shows? (Check network tab) |

---

## A02: Cryptographic Failures

**Risk**: Sensitive data is transmitted or stored without proper encryption.

| # | QA Check |
|---|----------|
| 2.1 | Is the site served over HTTPS? Does HTTP redirect to HTTPS? |
| 2.2 | Are passwords visible in network traffic? (Network tab during login) |
| 2.3 | Are sensitive values (tokens, passwords) in URL query strings? |
| 2.4 | Does the site set `Secure` flag on cookies? |
| 2.5 | Are API keys or secrets visible in page source or JS files? |

---

## A03: Injection

**Risk**: Untrusted data is sent to an interpreter (SQL, OS, LDAP) as a command.

| # | QA Check |
|---|----------|
| 3.1 | Do inputs like search, login, filters accept SQL special characters without error? (`'`, `"`, `;`, `--`) |
| 3.2 | Are raw SQL errors ever visible in the UI or API responses? |
| 3.3 | Do any inputs get reflected back in the page? (Search results, error messages) |
| 3.4 | Can you inject HTML/script into form fields and see it rendered? (XSS) |
| 3.5 | Do file path inputs accept `../` sequences? |

---

## A04: Insecure Design

**Risk**: Design flaws that can't be fixed by good implementation alone.

| # | QA Check |
|---|----------|
| 4.1 | Is there rate limiting on login attempts? (Try 50 rapid attempts) |
| 4.2 | Is there rate limiting on password reset requests? |
| 4.3 | Does the password reset flow use secure, time-limited tokens? |
| 4.4 | Can users enumerate valid accounts? (Different error for invalid email vs wrong password?) |
| 4.5 | Are there missing confirmation steps for destructive actions? (Delete, mass update) |

---

## A05: Security Misconfiguration

**Risk**: Default configurations, incomplete configs, or overly verbose error messages.

| # | QA Check |
|---|----------|
| 5.1 | Are stack traces or detailed error messages shown to users? |
| 5.2 | Are security headers present? (CSP, HSTS, X-Frame-Options — use `scripts/check_headers.py`) |
| 5.3 | Are default admin credentials changed? (admin/admin, admin/password) |
| 5.4 | Is directory listing enabled on the web server? (Try visiting `/uploads/`, `/static/`) |
| 5.5 | Are debug endpoints accessible in production? (`/debug`, `/actuator`, `/__debug__`) |

---

## A06: Vulnerable and Outdated Components

**Risk**: Using libraries with known CVEs.

| # | QA Check |
|---|----------|
| 6.1 | Run `scripts/scan_dependencies.py` on `package.json` or `requirements.txt` |
| 6.2 | Are any critical or high CVEs present in the dependency scan? |
| 6.3 | Are major framework versions severely out of date? (Check release notes) |

---

## A07: Identification and Authentication Failures

**Risk**: Weak authentication or session management.

| # | QA Check |
|---|----------|
| 7.1 | Does the session token change after login? (Session fixation check) |
| 7.2 | Are session cookies marked `HttpOnly` and `Secure`? |
| 7.3 | Does logout actually invalidate the session server-side? |
| 7.4 | Is there a brute force protection on login? |
| 7.5 | Are weak passwords accepted? (Try "password", "123456") |

---

## A08: Software and Data Integrity Failures

**Risk**: Untrusted code or data included without verification.

| # | QA Check |
|---|----------|
| 8.1 | Does the app load scripts from external CDNs without Subresource Integrity (SRI) checks? |
| 8.2 | Is there any auto-update functionality? Does it verify signatures? |
| 8.3 | Can user-uploaded files be served back as executable content? (Try uploading an HTML or JS file) |

---

## A09: Security Logging and Monitoring Failures

**Risk**: Attacks aren't detected or logged.

| # | QA Check |
|---|----------|
| 9.1 | Are failed login attempts logged? |
| 9.2 | Are there alerts for repeated authentication failures? |
| 9.3 | Are sensitive operations (admin actions, data exports) audited? |

---

## A10: Server-Side Request Forgery (SSRF)

**Risk**: App fetches a remote resource based on user-supplied URL.

| # | QA Check |
|---|----------|
| 10.1 | Are there any features where users supply URLs? (Preview, import, webhook) |
| 10.2 | Do those features attempt to fetch internal IP ranges? (Try `http://127.0.0.1`, `http://169.254.169.254`) |
| 10.3 | Can file:// or non-HTTP schemes be passed as URLs? |

---

## Summary Template

After completing the checklist:

| Risk | Status | Issues Found |
|------|--------|-------------|
| A01: Broken Access Control | ✅/❌/⚠️ | |
| A02: Cryptographic Failures | ✅/❌/⚠️ | |
| A03: Injection | ✅/❌/⚠️ | |
| A04: Insecure Design | ✅/❌/⚠️ | |
| A05: Security Misconfiguration | ✅/❌/⚠️ | |
| A06: Vulnerable Components | ✅/❌/⚠️ | |
| A07: Auth Failures | ✅/❌/⚠️ | |
| A08: Integrity Failures | ✅/❌/⚠️ | |
| A09: Logging Failures | ✅/❌/⚠️ | |
| A10: SSRF | ✅/❌/⚠️ | |