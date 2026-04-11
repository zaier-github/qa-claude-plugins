# Scoring Methodology

How to score each coverage gap to determine its strategic priority. The goal is to move
beyond "this file has 12% coverage" to "this file has 12% coverage AND is touched every
sprint AND is called by the checkout flow AND handles money."

---

## The Four Dimensions

Each gap is scored 1–3 on four dimensions. Higher = more urgent.

---

### Dimension 1: Change Velocity

How often does this code change? Untested code that changes frequently is where regressions
are born. Stable untested code is lower risk — it's debt, but quiet debt.

**How to measure:**
```bash
# Commits to a file in the last 90 days
git log --oneline --since="90 days ago" -- <file> | wc -l

# Commits in the last 12 months for longer-term view
git log --oneline --since="12 months ago" -- <file> | wc -l

# Authors who touched the file (many authors = more likely to have inconsistent assumptions)
git shortlog -sn --no-merges -- <file>
```

**Scoring:**
| Score | Commits (90d) | Meaning |
|-------|--------------|---------|
| 3 — High | 5+ | Changes frequently; regression risk is live |
| 2 — Medium | 2–4 | Occasional changes; moderate risk |
| 1 — Low | 0–1 | Stable; lower urgency |

**Note:** A file that hasn't changed in 2 years is still debt — but it's stable debt.
A file changed 3 times last week with no tests is an active hazard.

---

### Dimension 2: Feature Reach

How many features, flows, or other modules depend on this code? A shared utility with
wide reach is a single point of failure — one untested bug affects everything that touches it.

**How to measure:**
```bash
# Direct importers of a Python module
grep -rn "from <module> import\|import <module>" src/ --include="*.py" | wc -l

# JavaScript/TypeScript
grep -rn "from '<module>'\|require('<module>')" src/ --include="*.js" --include="*.ts" | wc -l

# Any language: check how many test files reference it
grep -rn "<class_or_function>" tests/ -l | wc -l
```

**Scoring:**
| Score | Importers / Callers | Meaning |
|-------|-------------------|---------|
| 3 — Wide | 10+ | Core shared code; failure affects many features |
| 2 — Medium | 3–9 | Moderate reach; used across a few features |
| 1 — Narrow | 1–2 | Isolated; used in one place |

**Heuristics for wide reach without counting:**
- It's in a `utils/`, `helpers/`, `core/`, or `common/` directory → likely wide
- It's a base class or mixin → likely wide
- It's a middleware, decorator, or hook → likely very wide
- It's imported in `__init__.py` or `index.js` at the package level → likely wide

---

### Dimension 3: Failure Impact

What's the blast radius if this code fails silently? Not all bugs are equal — a calculation
error in a financial module is categorically worse than a display formatting bug.

**This dimension requires judgment, not measurement.** Read the code and ask:
- Does this code write to a database? (data integrity risk)
- Does it handle money, pricing, or billing? (financial risk)
- Does it enforce authentication or authorization? (security risk)
- Does it send communications to users? (trust/reputation risk)
- Does it control user-facing behavior in a high-traffic path? (user experience risk)
- Does it have regulatory implications (PII, compliance logging)? (legal/compliance risk)
- Or is it logging, formatting, internal tooling, reporting? (lower impact)

**Scoring:**
| Score | Impact Profile |
|-------|---------------|
| 3 — Critical | Financial, auth/security, data writes, compliance, high-traffic user paths |
| 2 — Significant | Error handling, integrations, user notifications, business logic |
| 1 — Limited | Logging, display formatting, internal tooling, read-only reporting |

---

### Dimension 4: Domain Criticality

Beyond the specific code, how critical is the broader domain this code belongs to?
This provides a floor — even low-velocity, narrow-reach code in a critical domain
deserves more scrutiny than high-velocity code in a non-critical domain.

**Critical domains** (score 3):
- Payments, billing, subscriptions, refunds
- Authentication, authorization, session management
- Data migrations, schema changes, data integrity
- Regulatory compliance (GDPR, HIPAA, PCI, SOX)
- Core business logic (the thing the product primarily does)

**Significant domains** (score 2):
- User-facing APIs and core service integrations
- Notification and communication systems
- Search, recommendations, personalization
- Reporting and analytics that drive business decisions

**Supporting domains** (score 1):
- Internal admin tooling
- Development utilities, scripts, CLI tools
- Non-critical background jobs
- Documentation generation, formatting, display helpers

---

## Composite Score

```
Composite = (Velocity × 0.25) + (Reach × 0.25) + (Impact × 0.35) + (Domain × 0.15)
```

Impact is weighted highest because a low-velocity, narrow-reach payment bug is still
critical. Domain is lowest because it's a broad signal that the other dimensions refine.

**Risk tier thresholds:**

| Composite Score | Tier |
|----------------|------|
| 2.5 – 3.0 | 🔴 Danger Zone |
| 1.8 – 2.4 | 🟠 Watch List |
| 1.2 – 1.7 | 🟡 Backlog |
| 1.0 – 1.1 | 🟢 Low Priority |

**Override rules:**
- Any gap with Impact = 3 (financial, auth, data write) is *at least* 🟠, regardless of
  velocity or reach. Untested critical-impact code is never low priority.
- Any gap in a domain with a recent production incident is promoted one tier.
- Any gap with 0% branch coverage (not just line coverage) in an otherwise-covered file
  is promoted one tier — it means the tests don't verify the actual decision logic.

---

## Practical notes

You won't always have all four dimensions available. Approximate as needed:
- No git access? Estimate velocity from file age, complexity, and domain activity
- No call graph? Estimate reach from directory structure and naming conventions
- When uncertain, bias toward higher scores — the cost of missing a real risk exceeds
  the cost of flagging a false one

Document your assumptions when you approximate.