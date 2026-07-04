# Lingputation codebook registry

Schema-first infrastructure for executable linguistic codebooks.

The project treats a codebook as a versioned, citable specification: it defines an annotation target, output contract, decision rules, validation expectations, and a declared projectibility profile. The registry stores metadata and validation records, not corpus data.

## What It Is

- `schema/codebook.schema.json`: schema for codebook-as-program packages.
- `schema/validation-record.schema.json`: schema for validation, adjudication, and cross-instrument records.
- `schema/registry-entry.schema.json`: schema for citable registry metadata.
- `data/codebooks/`: versioned codebook packages.
- `data/validation-records/`: validation records linked to codebooks.
- `data/registry.jsonl`: one registry entry per line.
- `scripts/validate.py`: schema validator for JSON and JSONL files.
- `scripts/build_registry.py`: builds `registry.json` for the browser UI.
- `scripts/quality.py`: checks registry consistency beyond schema validity.
- `index.html`: static local browser over `registry.json`.

## Design Commitments

- Codebooks declare projection targets before validation claims.
- Model independence is an empirical question, not an assumption.
- Validation records distinguish human adjudication, instrument agreement, downstream checks, and known failure zones.
- Projectibility profiles state supported inferences, unsupported inferences, scope conditions, and demotion triggers.
- Toy/example records are marked as such and should not be cited as empirical validation.

## License

Software, scripts, schemas, and interface code are MIT licensed. Codebook specifications, validation-record content, registry metadata, examples, and documentation are CC BY 4.0 unless a registry entry states otherwise. See `LICENSE` and `LICENSE-CONTENT.md`.

## Workflow

1. Add or edit a codebook package in `data/codebooks/<id>/codebook.json`.
2. Add validation records in `data/validation-records/`.
3. Add or update the registry index in `data/registry.jsonl`.
4. Run validation:

```bash
python3 scripts/validate.py data/registry.jsonl schema/registry-entry.schema.json
python3 scripts/validate.py data/codebooks/example-intensifier/codebook.json schema/codebook.schema.json
python3 scripts/validate.py data/validation-records/example-intensifier-validation.json schema/validation-record.schema.json
```

5. Build and check the browser registry:

```bash
python3 scripts/build_registry.py data/registry.jsonl registry.json
python3 scripts/quality.py data/registry.jsonl registry.json
```

Open `index.html` in a browser to inspect the registry. If local browser restrictions block `fetch()`, run `python3 -m http.server` in this directory and open `http://localhost:8000/`.

## Status

This is an initial local scaffold. It is not a hosted registry and has no public governance model yet.

## Seeded Packages

- `example-intensifier-codebook`: toy infrastructure exemplar; not empirically validated.
- `cgelbank-category-function-core`: reviewed micro-package for CGELBank core category/function/projection conventions, with validation summarized from the published 50-sentence CGELBank interannotator-agreement study.
