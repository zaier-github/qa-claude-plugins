# Tool Format Guide

How to extract surviving mutant data from the output of common mutation testing tools.

---

## Mutmut (Python)

Mutmut stores results in a SQLite database (`.mutmut-cache`) and can produce multiple
output formats.

**List surviving mutants:**
```bash
mutmut results          # Summary counts
mutmut show all         # All mutants with status
mutmut show survived    # Only survivors (most useful)
```

**Export as text for analysis:**
```bash
# Show each surviving mutant with its diff
for id in $(mutmut results | grep "survived" | grep -oP '\d+'); do
  echo "=== Mutant $id ==="
  mutmut show $id
done

# Or use the HTML report
mutmut html
# Opens htmlcov/index.html — browse by file, shows original vs mutated code
```

**Key fields to extract per mutant:**
- Mutant ID
- File path and line number
- Original code (before mutation)
- Mutated code (the surviving variant)
- Status: `survived` | `killed` | `suspicious` | `timeout` | `skipped`

---

## Stryker (JavaScript / TypeScript)

Stryker produces a detailed HTML report and a JSON report.

**JSON report location:** `reports/mutation/mutation.json` (default)

**Structure:**
```json
{
  "files": {
    "src/billing/processor.js": {
      "mutants": [
        {
          "id": "42",
          "mutatorName": "ArithmeticOperator",
          "replacement": "-",
          "location": { "start": {"line": 15, "column": 22}, "end": {"line": 15, "column": 23} },
          "status": "Survived",
          "statusReason": null,
          "static": false,
          "coveredBy": ["test1"],
          "killedBy": []
        }
      ]
    }
  }
}
```

**Extract survivors:**
```javascript
const fs = require('fs');
const report = JSON.parse(fs.readFileSync('reports/mutation/mutation.json'));
for (const [file, data] of Object.entries(report.files)) {
  for (const mutant of data.mutants) {
    if (mutant.status === 'Survived') {
      console.log(`${file}:${mutant.location.start.line} [${mutant.mutatorName}] → "${mutant.replacement}"`);
    }
  }
}
```

**Stryker mutant statuses:**
- `Survived` → test gap (the ones to deliberate)
- `Killed` → tests caught it (good)
- `NoCoverage` → no test even executed this code (coverage gap — surface to Cartographer)
- `Timeout` → infinite loop introduced (often acquit as equivalent)
- `CompileError` → mutation broke syntax (acquit)
- `Ignored` → explicitly excluded

---

## PIT / Pitest (Java)

PIT generates XML and HTML reports. The XML is most parseable.

**XML report location:** `target/pit-reports/<timestamp>/mutations.xml`

**Structure:**
```xml
<mutations>
  <mutation detected="false" status="SURVIVED" numberOfTestsRun="5">
    <sourceFile>DiscountEngine.java</sourceFile>
    <mutatedClass>com.example.billing.DiscountEngine</mutatedClass>
    <mutatedMethod>applyDiscount</mutatedMethod>
    <mutatedMethodDesc>(DLjava/lang/String;)D</mutatedMethodDesc>
    <lineNumber>47</lineNumber>
    <mutator>org.pitest.mutationtest.engine.gregor.mutators.ArithmeticOperatorReplacementMutator</mutator>
    <index>3</index>
    <block>2</block>
    <description>Replaced double addition with subtraction</description>
  </mutation>
</mutations>
```

**Extract survivors:**
```bash
python3 -c "
import xml.etree.ElementTree as ET
tree = ET.parse('mutations.xml')
for m in tree.findall('.//mutation[@status=\"SURVIVED\"]'):
    file = m.findtext('sourceFile')
    method = m.findtext('mutatedMethod')
    line = m.findtext('lineNumber')
    desc = m.findtext('description')
    print(f'{file}::{method}:{line} — {desc}')
"
```

---

## Cosmic Ray (Python)

Cosmic Ray stores results in a database and can export as JSON or text.

```bash
cosmic-ray dump <session-file> | python -m json.tool   # JSON output
cosmic-ray report <session-file>                        # Human-readable summary
```

**JSON structure per work item:**
```json
{
  "work_item": {
    "module_path": "src/billing/processor",
    "operator_name": "cosmic_ray.operators.arithmetic_operator_replacement",
    "occurrence": 2
  },
  "job_outcome": {
    "outcome": "survived",
    "worker_outcome": "normal",
    "output": ""
  }
}
```

---

## cargo-mutants (Rust)

```bash
cargo mutants                           # Run and save results
cat mutants.out/outcomes.json           # JSON results
```

**JSON structure:**
```json
{
  "mutants": [
    {
      "file": "src/billing/processor.rs",
      "function": "apply_discount",
      "line": 47,
      "col": 12,
      "mutation": "replace return value with Default::default()",
      "outcome": "missed"
    }
  ]
}
```

Statuses: `missed` = survived, `caught` = killed, `unviable` = compile error (acquit).

---

## infection (PHP)

```bash
vendor/bin/infection --log-verbosity=all
cat infection.log   # or infection.json
```

**JSON log structure:**
```json
{
  "stats": { "totalMutantsCount": 100, "killedCount": 72, "escapedCount": 18, ... },
  "escaped": [
    {
      "mutator": { "mutatorName": "GreaterThanOrEqualTo", "description": "..." },
      "diff": "--- Original\n+++ New\n...",
      "processOutput": "...",
      "originalFilePath": "src/Billing/Processor.php",
      "originalStartingLine": 47
    }
  ]
}
```

---

## Handling raw terminal output (any tool)

If the user pastes raw terminal output rather than a structured report, look for these
patterns:

```
# Common terminal output patterns across tools
SURVIVED  src/billing/processor.py:47 - replaced + with -
SURVIVED  billing/Processor.java:47 - Replaced integer addition with subtraction
Mutant #42 survived: billing/processor.js:15 ArithmeticOperator → "-"
```

Extract: file, line number, operator type, and the specific code change. If the terminal
output doesn't include the actual code diff, ask the user to run `show <id>` or provide
the file for direct inspection.

---

## When no report is provided

If the user only has a summary ("we have 143 surviving mutants, mutation score 54%"),
use the Strategy Report template (`references/strategy-report-template.md`) instead
of the Verdict Report. Produce guidance on what to measure and how to prioritize
without individual mutant data.