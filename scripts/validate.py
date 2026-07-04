#!/usr/bin/env python3
"""
Validate a JSON or JSONL file against a JSON Schema.

Usage:
  python3 scripts/validate.py data/registry.jsonl schema/registry-entry.schema.json
  python3 scripts/validate.py data/codebooks/example-intensifier/codebook.json schema/codebook.schema.json
"""
import json
import sys
from pathlib import Path

try:
    import jsonschema
except ImportError:
    print("Missing dependency: jsonschema. Install with: pip install jsonschema", file=sys.stderr)
    sys.exit(2)


def load_records(path: Path):
    if path.suffix == ".jsonl":
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            try:
                yield line_number, json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"[line {line_number}] JSON decode error: {exc}") from exc
        return

    try:
        yield 1, json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path}: JSON decode error: {exc}") from exc


def record_id(record: dict) -> str:
    for key in ("registry_id", "id", "codebook_id"):
        if key in record:
            return str(record[key])
    return "<missing-id>"


def main(input_path: Path, schema_path: Path) -> int:
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(schema)
    ok = True

    try:
        records = list(load_records(input_path))
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    for line_number, record in records:
        errors = sorted(validator.iter_errors(record), key=lambda err: list(err.path))
        if not errors:
            continue
        ok = False
        print(f"[record {line_number}] id={record_id(record)}", file=sys.stderr)
        for error in errors:
            path = ".".join(str(part) for part in error.path) if error.path else "<root>"
            print(f"  - {path}: {error.message}", file=sys.stderr)

    if ok:
        print(f"OK: {input_path} validates against {schema_path}.")
        return 0
    return 1


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__.strip(), file=sys.stderr)
        sys.exit(2)
    sys.exit(main(Path(sys.argv[1]), Path(sys.argv[2])))

