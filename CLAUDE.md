# CLAUDE.md

## Purpose

Local infrastructure for a lingputation codebook registry: executable codebook packages, validation records, and citable registry entries.

## Role

Claude's role in this project is **Developer**. It can edit schemas, scripts, documentation, and local example packages. It should not invent empirical validation results or create public release state without Brett's explicit instruction.

## Validation Commands

```bash
python3 scripts/validate.py data/registry.jsonl schema/registry-entry.schema.json
python3 scripts/validate.py data/codebooks/example-intensifier/codebook.json schema/codebook.schema.json
python3 scripts/validate.py data/validation-records/example-intensifier-validation.json schema/validation-record.schema.json
python3 scripts/build_registry.py data/registry.jsonl registry.json
python3 scripts/build_registry.py data/registry.jsonl registry.json --check
python3 scripts/quality.py data/registry.jsonl registry.json
```

## Non-Negotiables

- Keep toy records visibly toy.
- Real validation requires source material.
- Projectibility claims must say what inference is licensed and under what scope.
- Failure zones and unsupported inferences are first-class fields, not caveat prose.

