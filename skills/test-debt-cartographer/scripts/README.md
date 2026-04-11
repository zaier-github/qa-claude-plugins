# Scripts: Generating Coverage Reports

Commands to generate coverage reports for common stacks when no report is pre-provided.
Run from the repository root unless noted otherwise.

---

## Python (pytest-cov)

```bash
# Install if needed
pip install pytest-cov

# Generate XML report (parseable)
pytest --cov=src --cov-report=xml:coverage.xml --cov-report=term-missing

# Generate with branch coverage (preferred — reveals more gaps)
pytest --cov=src --cov-branch --cov-report=xml:coverage.xml

# Generate lcov format
pytest --cov=src --cov-branch --cov-report=lcov:coverage.lcov

# Show uncovered lines in terminal
pytest --cov=src --cov-report=term-missing:skip-covered
```

---

## JavaScript / TypeScript (Jest)

```bash
# Run with coverage (outputs to coverage/ directory)
npx jest --coverage

# Specify output format
npx jest --coverage --coverageReporters=json-summary --coverageReporters=lcov

# Generate summary JSON (easiest to parse)
npx jest --coverage --coverageReporters=json-summary
# Output: coverage/coverage-summary.json
```

---

## JavaScript / TypeScript (Vitest)

```bash
npx vitest run --coverage
# Output: coverage/ directory with lcov.info and index.html
```

---

## JavaScript / TypeScript (NYC / Istanbul)

```bash
# With Mocha
npx nyc mocha

# Generate specific formats
npx nyc --reporter=json-summary --reporter=lcov mocha
# Output: coverage/coverage-summary.json and coverage/lcov.info
```

---

## Ruby (SimpleCov)

Add to `spec_helper.rb` or `test_helper.rb`:
```ruby
require 'simplecov'
SimpleCov.start do
  add_filter '/spec/'
  add_filter '/test/'
end
```

Then run tests normally:
```bash
bundle exec rspec
# Output: coverage/.resultset.json and coverage/index.html
```

---

## Go

```bash
# Generate coverage profile
go test ./... -coverprofile=coverage.out -covermode=atomic

# View as percentage by package
go tool cover -func=coverage.out

# Generate HTML report
go tool cover -html=coverage.out -o coverage.html

# Coverage with race detection (recommended)
go test -race ./... -coverprofile=coverage.out
```

---

## Rust

```bash
# Using cargo-tarpaulin (install once)
cargo install cargo-tarpaulin

# Generate lcov report
cargo tarpaulin --out Lcov --output-dir coverage/

# Generate with branch coverage
cargo tarpaulin --out Lcov --output-dir coverage/ --branches
```

---

## Java (JaCoCo with Maven)

```xml
<!-- Add to pom.xml -->
<plugin>
  <groupId>org.jacoco</groupId>
  <artifactId>jacoco-maven-plugin</artifactId>
  <version>0.8.11</version>
</plugin>
```

```bash
mvn test jacoco:report
# Output: target/site/jacoco/jacoco.xml
```

---

## .NET (Coverlet)

```bash
dotnet test --collect:"XPlat Code Coverage"
# Output: TestResults/**/*.xml (Cobertura format)

# Or with specific format
dotnet test /p:CollectCoverage=true /p:CoverletOutputFormat=lcov /p:CoverletOutput=./coverage/
```

---

## Notes

- Always use branch coverage (`--cov-branch`, `--branches`, etc.) when available.
  Line coverage alone misses conditional logic gaps.
- Run from a clean state — stale `.pyc` files or cached test results can skew numbers.
- If the project uses a monorepo structure, run coverage per-service rather than
  globally to avoid diluting the numbers across unrelated modules.