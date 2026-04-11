# CSV Import Guide

Covers two target platforms: **Xray** (Jira-native) and **TestRail**. Ask the user which platform to export for, or generate both. Output file names differ per platform.

---

## Xray

### Column headers (exact, copy verbatim)

```
Test Key,Summary,Test Type,Priority,Labels,Preconditions,Steps,Expected Result,Requirement Keys,Folder Path
```

### Field rules

| Column               | Rules                                                              |
|----------------------|--------------------------------------------------------------------|
| **Test Key**         | Leave **empty** — Xray auto-generates. Do NOT put the TC-ID here.  |
| **Summary**          | Concise test title. No quotes needed unless it contains a comma.   |
| **Test Type**        | Always `Manual` for manual tests                                   |
| **Priority**         | `P1`, `P2`, `P3`, or `P4` — no other values                        |
| **Labels**           | Comma-separated tags without spaces: `login,auth,regression`       |
| **Preconditions**    | Bullet list with `\n` between items: `• Item 1\n• Item 2`          |
| **Steps**            | Pipe-separated, one per line: see step format below                |
| **Expected Result**  | Final overall expected result (not per-step)                       |
| **Requirement Keys** | Jira issue key: `PROJ-123`                                         |
| **Folder Path**      | Xray test folder path starting with `/`: `/Login` or `/`           |

### Step format

Each step occupies one line within the Steps cell:

```
{Number}|{Action}|{Data}|{Expected Result}
```

Multiple steps are separated by `\n`:

```
1|Navigate to the login page||Login page is displayed
2|Enter <VALID_EMAIL> in the Email field|<VALID_EMAIL>|Email is accepted
3|Enter <VALID_PASSWORD> in the Password field|<VALID_PASSWORD>|Password is masked
4|Click the Login button||Authentication begins
5|Verify redirect to dashboard||Dashboard page loads
```

### Escaping rules

- Fields containing **commas**: wrap entire field in double quotes: `"login,auth,regression"`
- Fields containing **double quotes**: escape as `""` within a quoted field: `"He said ""hello"""`
- Fields containing **newlines** (`\n`): wrap in double quotes

### Complete row example

```csv
,"Verify successful login with valid credentials",Manual,P1,"login,auth,regression","• Registered user account exists\n• Application is accessible","1|Navigate to login page||Login form displays\n2|Enter <VALID_EMAIL>|<VALID_EMAIL>|Email accepted\n3|Enter <VALID_PASSWORD>|<VALID_PASSWORD>|Password masked\n4|Click Login button||Authentication starts\n5|Verify redirect to /dashboard||Dashboard loads","User authenticated; dashboard displays personalized content","PROJ-123","/"
```

### Generating the file

- First row: header row (exact column names above)
- One row per test case
- File name: `xray-bulk-import.csv`
- Encoding: UTF-8

---

## TestRail

### Column headers (exact, copy verbatim)

```
Title,Section,Type,Priority,Estimate,References,Preconditions,Steps,Expected Result
```

### Field rules

| Column            | Rules                                                                                       |
|-------------------|---------------------------------------------------------------------------------------------|
| **Title**         | Concise test title. Same as the test case summary.                                          |
| **Section**       | Folder path using ` > ` as separator: `Login > Authentication`. Use single name for root.   |
| **Type**          | `Functional` for most cases. Use `Acceptance` for happy-path, `Regression` for suite tests. |
| **Priority**      | Map from internal priority: P1 → `Critical`, P2 → `High`, P3 → `Medium`, P4 → `Low`        |
| **Estimate**      | Time estimate in TestRail format: `30s`, `5m`, `1h 30m`. Omit if unknown.                  |
| **References**    | Jira issue key: `PROJ-123`. Multiple keys separated by commas.                              |
| **Preconditions** | Plain text. Use newlines (`\n`) between items.                                              |
| **Steps**         | One action per line, separated by `\n`. Plain text — no pipe delimiters.                   |
| **Expected Result** | One expected result per step line, separated by `\n`. Must have the same line count as Steps. |

### Priority mapping

| Internal | TestRail  |
|----------|-----------|
| P1       | Critical  |
| P2       | High      |
| P3       | Medium    |
| P4       | Low       |

### Step format

Steps and expected results are newline-separated plain strings. Each `\n` in the Steps cell corresponds to one step; the matching line in Expected Result covers that step:

```
Steps cell:
Navigate to the login page\nEnter <VALID_EMAIL> in the Email field\nEnter <VALID_PASSWORD> in the Password field\nClick the Login button\nVerify redirect to dashboard

Expected Result cell:
Login page is displayed\nEmail is accepted\nPassword is masked\nAuthentication begins\nDashboard page loads
```

### Escaping rules

Same CSV escaping as Xray:
- Fields containing **commas**: wrap entire field in double quotes
- Fields containing **double quotes**: escape as `""` within a quoted field
- Fields containing **newlines** (`\n`): wrap in double quotes

### Complete row example

```csv
"Verify successful login with valid credentials","Login > Authentication",Acceptance,Critical,5m,"PROJ-123","Registered user account exists\nApplication is accessible","Navigate to the login page\nEnter <VALID_EMAIL> in the Email field\nEnter <VALID_PASSWORD> in the Password field\nClick the Login button\nVerify redirect to /dashboard","Login page is displayed\nEmail is accepted\nPassword is masked\nAuthentication begins\nDashboard page loads with personalized content"
```

### Generating the file

- First row: header row (exact column names above)
- One row per test case
- File name: `testrail-import.csv`
- Encoding: UTF-8
