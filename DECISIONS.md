# Decisions

2026-07-04 -- Created a local schema-first infrastructure project rather than a hosted app. Reason: the bottleneck is the citable codebook package and validation surface, not storage or UI.

2026-07-04 -- Used `tools/glottocode_registry_prototype/` as the closest local pattern. Reason: it already proves the JSON Schema + JSONL + validator + static UI shape works in this workspace.

2026-07-04 -- Marked the exemplar as a toy infrastructure object. Reason: source-grounding rules forbid treating invented examples or placeholder validation as empirical evidence.

2026-07-04 -- Published the scaffold as public GitHub repository `BrettRey/lingputation-codebook-registry`. Reason: Brett asked to make the infrastructure public.

2026-07-04 -- Documented a license split: MIT for software, scripts, schemas, and interface code; CC BY 4.0 for codebook specifications, registry metadata, validation-record content, examples, and documentation unless a registry entry states otherwise. Reason: this is both software infrastructure and a scholarly registry/content format.
