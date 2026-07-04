#!/usr/bin/env python3
"""
Cross-file quality checks for the lingputation registry.

Usage:
  python3 scripts/quality.py data/registry.jsonl [registry.json]
"""
import json
import sys
from datetime import date
from pathlib import Path


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path):
    records = []
    errors = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            records.append((line_number, json.loads(line)))
        except json.JSONDecodeError as exc:
            errors.append(f"[line {line_number}] JSON decode error: {exc}")
    return records, errors


def parse_date(value: str, field: str, line_number: int, errors: list[str]):
    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError):
        errors.append(f"[line {line_number}] invalid date in {field}: {value}")
        return None


def duplicate_values(values: list[str]) -> list[str]:
    seen = set()
    duplicates = []
    for value in values:
        if value in seen and value not in duplicates:
            duplicates.append(value)
        seen.add(value)
    return duplicates


def project_root(registry_path: Path) -> Path:
    if registry_path.parent.name == "data":
        return registry_path.parent.parent
    return registry_path.parent


def main(registry_path: Path, web_path: Path | None = None) -> int:
    entries, parse_errors = load_jsonl(registry_path)
    errors = list(parse_errors)
    warnings = []
    root = project_root(registry_path)

    registry_ids = []
    codebook_versions = []

    for line_number, entry in entries:
        registry_id = entry.get("registry_id")
        codebook_id = entry.get("codebook_id")
        codebook_version = entry.get("codebook_version")
        registry_ids.append(registry_id)
        codebook_versions.append(f"{codebook_id}@{codebook_version}")

        created = parse_date(entry.get("created"), "created", line_number, errors)
        updated = parse_date(entry.get("updated"), "updated", line_number, errors)
        if created and updated and updated < created:
            errors.append(f"[line {line_number}] updated precedes created")

        codebook_path = root / entry.get("codebook_path", "")
        if not codebook_path.exists():
            errors.append(f"[line {line_number}] missing codebook_path: {codebook_path}")
        else:
            try:
                codebook = load_json(codebook_path)
                if codebook.get("id") != codebook_id:
                    errors.append(f"[line {line_number}] codebook_id does not match {codebook_path}")
                if codebook.get("version") != codebook_version:
                    errors.append(f"[line {line_number}] codebook_version does not match {codebook_path}")
                profile = codebook.get("projectibility_profile", {})
                for field in ("supported_inferences", "unsupported_inferences", "failure_zones", "demotion_triggers"):
                    if not profile.get(field):
                        errors.append(f"[line {line_number}] codebook projectibility_profile.{field} is empty")
            except json.JSONDecodeError as exc:
                errors.append(f"[line {line_number}] codebook JSON decode error: {exc}")

        validation_refs = entry.get("validation_records", [])
        if not any(ref.get("status") == "complete" for ref in validation_refs):
            warnings.append(f"[line {line_number}] no complete validation record yet")
        for ref in validation_refs:
            validation_path = root / ref.get("path", "")
            if not validation_path.exists():
                errors.append(f"[line {line_number}] missing validation record: {validation_path}")
                continue
            try:
                validation = load_json(validation_path)
            except json.JSONDecodeError as exc:
                errors.append(f"[line {line_number}] validation JSON decode error: {exc}")
                continue
            if validation.get("id") != ref.get("id"):
                errors.append(f"[line {line_number}] validation id mismatch: {validation_path}")
            if validation.get("codebook_id") != codebook_id:
                errors.append(f"[line {line_number}] validation codebook_id mismatch: {validation_path}")
            if validation.get("codebook_version") != codebook_version:
                errors.append(f"[line {line_number}] validation codebook_version mismatch: {validation_path}")

        for field in ("supported_inferences", "unsupported_inferences", "scope_conditions", "failure_zones"):
            values = entry.get("projectibility_profile", {}).get(field, [])
            dupes = duplicate_values(values)
            if dupes:
                warnings.append(f"[line {line_number}] duplicate projectibility_profile.{field}: {', '.join(dupes)}")

        for link in entry.get("links", []):
            url = link.get("url", "")
            if url and not (url.startswith("https://") or url.startswith("http://localhost")):
                warnings.append(f"[line {line_number}] non-https external link: {url}")

    for duplicate in duplicate_values([value for value in registry_ids if value]):
        errors.append(f"duplicate registry_id: {duplicate}")
    for duplicate in duplicate_values([value for value in codebook_versions if value]):
        errors.append(f"duplicate codebook/version pair: {duplicate}")

    if web_path:
        if not web_path.exists():
            errors.append(f"missing registry JSON: {web_path}")
        else:
            try:
                web_records = load_json(web_path)
                expected = [entry for _, entry in entries]
                expected = sorted(expected, key=lambda item: (item.get("title", ""), item.get("registry_id", "")))
                if web_records != expected:
                    errors.append(f"{web_path} is out of sync with {registry_path}")
            except json.JSONDecodeError as exc:
                errors.append(f"{web_path} JSON decode error: {exc}")

    if warnings:
        print("Warnings:")
        for warning in warnings:
            print(f"  - {warning}")

    if errors:
        print("Errors:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print("OK: quality checks passed.")
    return 0


if __name__ == "__main__":
    if len(sys.argv) not in {2, 3}:
        print(__doc__.strip(), file=sys.stderr)
        sys.exit(2)
    registry = Path(sys.argv[1])
    web = Path(sys.argv[2]) if len(sys.argv) == 3 else None
    sys.exit(main(registry, web))

