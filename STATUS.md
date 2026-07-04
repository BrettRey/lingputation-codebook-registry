# Lingputation Codebook Registry

**Status:** Initial local scaffold
**Last Updated:** 2026-07-04
**Repository:** https://github.com/BrettRey/lingputation-codebook-registry

## Project Summary

Minimal infrastructure for a registry of executable linguistic codebooks. The first target is a local, citable package format with validation records and declared projectibility profiles.

## Current State

- [x] Project scaffold created.
- [x] Codebook schema drafted.
- [x] Validation-record schema drafted.
- [x] Registry-entry schema drafted.
- [x] Toy exemplar codebook included.
- [x] Toy validation-record template included.
- [x] Static registry UI included.
- [x] Public GitHub repository created.
- [x] License split documented: MIT for software/infrastructure; CC BY 4.0 for content/metadata unless otherwise stated.
- [x] First real codebook package added: CGELBank core category/function package.
- [x] Complete source-literature validation record added for the published CGELBank IAA study.
- [ ] Governance model defined.

## Files

| File | Purpose |
|------|---------|
| `schema/codebook.schema.json` | Schema for codebook-as-program packages |
| `schema/validation-record.schema.json` | Schema for validation/adjudication records |
| `schema/registry-entry.schema.json` | Schema for registry metadata |
| `data/registry.jsonl` | Registry index |
| `scripts/validate.py` | Schema validator |
| `scripts/build_registry.py` | Builds `registry.json` for the UI |
| `scripts/quality.py` | Cross-file consistency and quality checks |
| `index.html` | Static browser UI |

## Next Actions

1. Define governance before inviting contributions.
2. Decide whether to enable GitHub Pages for the static registry UI.
3. Add a pinned-rerun validation record for a specific CGELBank repository commit if this becomes more than a literature-summary package.
4. Choose the next real codebook after CGELBank, preferably one with an LLM/hybrid preannotation layer.
