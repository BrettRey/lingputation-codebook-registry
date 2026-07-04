#!/usr/bin/env python3
"""
Build registry.json from the JSONL registry.

Usage:
  python3 scripts/build_registry.py data/registry.jsonl registry.json
  python3 scripts/build_registry.py data/registry.jsonl registry.json --check
"""
import json
import sys
from pathlib import Path


def load_jsonl(path: Path) -> list[dict]:
    records = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"[line {line_number}] JSON decode error: {exc}") from exc
    return records


def main(registry_path: Path, output_path: Path, check: bool) -> int:
    try:
        records = load_jsonl(registry_path)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    records = sorted(records, key=lambda item: (item.get("title", ""), item.get("registry_id", "")))

    if check:
        if not output_path.exists():
            print(f"Missing output file: {output_path}", file=sys.stderr)
            return 1
        try:
            existing = json.loads(output_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            print(f"Output JSON decode error: {exc}", file=sys.stderr)
            return 1
        if existing != records:
            print(f"{output_path} is out of sync with {registry_path}", file=sys.stderr)
            return 1
        print("OK: registry JSON is in sync.")
        return 0

    output_path.write_text(json.dumps(records, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) not in {2, 3}:
        print(__doc__.strip(), file=sys.stderr)
        sys.exit(2)
    check = len(args) == 3 and args[2] == "--check"
    if len(args) == 3 and not check:
        print("Unknown option. Use --check.", file=sys.stderr)
        sys.exit(2)
    sys.exit(main(Path(args[0]), Path(args[1]), check))

