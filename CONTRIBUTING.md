# Contributing

This repository stores metadata, codebook specifications, and validation records. It does not store restricted corpora or private annotation data.

## Add A Codebook

1. Create `data/codebooks/<codebook-id>/codebook.json`.
2. Validate it:

```bash
python3 scripts/validate.py data/codebooks/<codebook-id>/codebook.json schema/codebook.schema.json
```

3. Add at least one validation record or template under `data/validation-records/`.
4. Add a registry entry to `data/registry.jsonl`.
5. Rebuild and check:

```bash
python3 scripts/build_registry.py data/registry.jsonl registry.json
python3 scripts/quality.py data/registry.jsonl registry.json
```

## Required Intellectual Content

A codebook should state:

- what is being annotated;
- what inference the labels are meant to support;
- the output schema;
- decision rules for hard cases;
- uncertainty handling;
- validation expectations;
- supported and unsupported downstream inferences;
- failure zones and demotion triggers.

## Review Standard

Schema validity is necessary but not sufficient. A registry entry should be rejected or kept as draft if its projectibility profile is vague, if validation claims are unsupported, or if toy examples are presented as empirical evidence.

