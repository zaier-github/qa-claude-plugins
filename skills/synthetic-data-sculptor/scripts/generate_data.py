#!/usr/bin/env python3
"""
generate_data.py — Generate synthetic test data from a schema definition.

Usage:
  python scripts/generate_data.py --schema <schema.json> --count 100 --format json --output out.json
  python scripts/generate_data.py --schema <schema.json> --count 50 --scenario "users over 65 in Canada" --output out.json
  python scripts/generate_data.py --schema <schema.json> --edge-cases --output edge.json

Requires: pip install faker --break-system-packages
"""
import argparse
import csv
import json
import os
import random
import sys
import uuid
from datetime import datetime, timedelta, date


def ensure_faker():
    try:
        from faker import Faker
        return Faker()
    except ImportError:
        print("Faker not installed. Run: pip install faker --break-system-packages")
        sys.exit(1)


def load_schema(schema_path: str) -> dict:
    with open(schema_path) as f:
        return json.load(f)


def generate_value(field: dict, fake, context: dict = None) -> object:
    """Generate a single field value based on its definition."""
    field_type = field.get("type", "string")
    required = field.get("required", True)

    # Randomly leave optional fields null (~15% of the time)
    if not required and random.random() < 0.15:
        return None

    if field_type == "uuid":
        return str(uuid.uuid4())

    elif field_type == "string":
        max_len = field.get("max_length", 255)
        if "enum" in field:
            return random.choice(field["enum"])
        # Generic string
        val = fake.word()
        return val[:max_len]

    elif field_type == "email":
        return fake.email()

    elif field_type == "phone":
        return fake.phone_number()

    elif field_type == "date":
        # Parse min/max hints
        if field.get("max") == "today - 18 years":
            end = date.today() - timedelta(days=18 * 365)
        else:
            end = date(2005, 1, 1)
        start = date(1940, 1, 1)
        delta = (end - start).days
        return (start + timedelta(days=random.randint(0, delta))).isoformat()

    elif field_type == "datetime":
        if field.get("auto") == "now":
            return datetime.now().isoformat()
        # Random recent datetime
        days_back = random.randint(0, 730)
        dt = datetime.now() - timedelta(days=days_back, hours=random.randint(0, 23))
        return dt.isoformat()

    elif field_type == "boolean":
        return random.choice([True, False])

    elif field_type == "integer":
        min_val = field.get("min", 0)
        max_val = field.get("max", 1000)
        return random.randint(min_val, max_val)

    elif field_type == "float":
        min_val = field.get("min", 0.0)
        max_val = field.get("max", 1000.0)
        return round(random.uniform(min_val, max_val), 2)

    elif field_type == "enum":
        return random.choice(field.get("values", ["value1"]))

    return None


def generate_edge_cases(schema: dict) -> list[dict]:
    """Generate a targeted set of edge-case records."""
    from pathlib import Path
    catalog_path = Path(__file__).parent.parent / "references" / "edge_case_catalog.md"

    edge_records = []
    fields = schema.get("fields", [])
    fake = ensure_faker()

    # Base record with all normal values
    base = {f["name"]: generate_value(f, fake) for f in fields}

    string_fields = [f for f in fields if f.get("type") in ("string", "email", "phone")]
    date_fields = [f for f in fields if f.get("type") in ("date", "datetime")]

    edge_strings = [
        "",                             # Empty
        " ",                            # Whitespace only
        "O'Brien",                      # Apostrophe
        "<script>alert(1)</script>",    # XSS
        "A" * 256,                      # Over common VARCHAR limit
        "مرحبا بالعالم",               # Arabic RTL
        "שלום עולם",                    # Hebrew RTL
        "你好世界",                     # Chinese CJK
        "🚀💯🎉",                       # Emoji
        "'; DROP TABLE users; --",      # SQL injection
        "\0nullbyte",                   # Null byte
    ]

    edge_dates = [
        "1900-01-01", "1970-01-01", "2000-02-29",
        "2038-01-19", "2099-12-31"
    ]

    # One record per string edge case
    for edge_val in edge_strings:
        record = dict(base)
        for f in string_fields[:2]:  # Apply to first two string fields
            max_len = f.get("max_length", 999)
            record[f["name"]] = edge_val[:max_len] if f.get("type") == "string" else fake.email()
        edge_records.append(record)

    # One record per date edge case
    for edge_date in edge_dates:
        record = dict(base)
        for f in date_fields[:1]:
            record[f["name"]] = edge_date
        edge_records.append(record)

    # All-null optional fields record
    null_record = {}
    for f in fields:
        if f.get("required", True):
            null_record[f["name"]] = generate_value(f, fake)
        else:
            null_record[f["name"]] = None
    edge_records.append(null_record)

    return edge_records


def generate_records(schema: dict, count: int, scenario: str = None) -> list[dict]:
    fake = ensure_faker()
    fields = schema.get("fields", [])
    records = []

    for _ in range(count):
        record = {}
        for field in fields:
            if field.get("auto") == "now":
                record[field["name"]] = datetime.now().isoformat()
            else:
                record[field["name"]] = generate_value(field, fake)
        records.append(record)

    # Apply scenario hints (basic implementation — extend with LLM call if needed)
    if scenario:
        scenario_lower = scenario.lower()
        for record in records:
            if "over 65" in scenario_lower or "elderly" in scenario_lower:
                if "date_of_birth" in record:
                    years_ago = random.randint(65, 90)
                    record["date_of_birth"] = (date.today() - timedelta(days=years_ago * 365)).isoformat()
            if "canada" in scenario_lower or "ca" in scenario_lower:
                if "country_code" in record:
                    record["country_code"] = "CA"
            if "inactive" in scenario_lower:
                if "account_status" in record:
                    record["account_status"] = "inactive"

    return records


def to_sql(records: list[dict], table_name: str) -> str:
    if not records:
        return ""
    lines = []
    for r in records:
        cols = ", ".join(r.keys())
        vals = ", ".join(
            "NULL" if v is None else
            f"'{str(v).replace(chr(39), chr(39)+chr(39))}'" if isinstance(v, str) else
            str(v).lower() if isinstance(v, bool) else
            str(v)
            for v in r.values()
        )
        lines.append(f"INSERT INTO {table_name} ({cols}) VALUES ({vals});")
    return "\n".join(lines)


def to_csv(records: list[dict]) -> str:
    import io
    if not records:
        return ""
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=records[0].keys())
    writer.writeheader()
    writer.writerows(records)
    return output.getvalue()


def main():
    parser = argparse.ArgumentParser(description="Generate synthetic test data")
    parser.add_argument("--schema", required=True, help="Path to schema JSON file")
    parser.add_argument("--count", type=int, default=10, help="Number of records to generate")
    parser.add_argument("--format", choices=["json", "csv", "sql"], default="json")
    parser.add_argument("--output", required=True, help="Output file path")
    parser.add_argument("--scenario", default=None, help="Scenario description (e.g., 'users over 65 in Canada')")
    parser.add_argument("--edge-cases", action="store_true", help="Generate edge case records instead")
    parser.add_argument("--table", default="records", help="Table name for SQL output")
    args = parser.parse_args()

    schema = load_schema(args.schema)

    if args.edge_cases:
        records = generate_edge_cases(schema)
        print(f"Generated {len(records)} edge-case records")
    else:
        records = generate_records(schema, args.count, args.scenario)
        print(f"Generated {args.count} records" + (f" (scenario: {args.scenario})" if args.scenario else ""))

    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)

    if args.format == "json":
        with open(args.output, "w") as f:
            json.dump(records, f, indent=2, default=str)
    elif args.format == "csv":
        with open(args.output, "w") as f:
            f.write(to_csv(records))
    elif args.format == "sql":
        with open(args.output, "w") as f:
            f.write(to_sql(records, args.table))

    print(f"Saved to: {args.output}")


if __name__ == "__main__":
    main()