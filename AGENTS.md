# Agent Guidance

## Project Role

Agents working here are developers for a local research-methods tool. Keep edits focused on the registry infrastructure: schemas, validation scripts, codebook packages, validation records, and documentation.

## Source Grounding

Do not invent empirical linguistic data, citations, statistics, agreement scores, or model results. Toy records must be marked as toy/template records. Real validation records require source files or analysis outputs.

## Structure

- `schema/`: JSON Schemas. Keep `additionalProperties: false` unless there is a deliberate extension point.
- `data/codebooks/`: one directory per codebook package.
- `data/validation-records/`: validation records linked to codebooks.
- `data/registry.jsonl`: registry index, one JSON object per line.
- `registry.json`: generated from `data/registry.jsonl`; keep it in sync.
- `scripts/`: validation/build/quality tools.

## Commands

```bash
python3 scripts/validate.py data/registry.jsonl schema/registry-entry.schema.json
python3 scripts/validate.py data/codebooks/example-intensifier/codebook.json schema/codebook.schema.json
python3 scripts/validate.py data/validation-records/example-intensifier-validation.json schema/validation-record.schema.json
python3 scripts/build_registry.py data/registry.jsonl registry.json
python3 scripts/build_registry.py data/registry.jsonl registry.json --check
python3 scripts/quality.py data/registry.jsonl registry.json
```

## Edit Rules

- Preserve projectibility discipline: projection target, validation evidence, scope, failure zones, and demotion triggers are separate fields.
- Do not collapse cross-model agreement into validity. It is one validation source.
- Do not describe a codebook as model-independent unless validation records support that claim.
- Run validation after schema, registry, or data changes.

