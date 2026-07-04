# Decisions

2026-07-04 -- Created a local schema-first infrastructure project rather than a hosted app. Reason: the bottleneck is the citable codebook package and validation surface, not storage or UI.

2026-07-04 -- Used `tools/glottocode_registry_prototype/` as the closest local pattern. Reason: it already proves the JSON Schema + JSONL + validator + static UI shape works in this workspace.

2026-07-04 -- Marked the exemplar as a toy infrastructure object. Reason: source-grounding rules forbid treating invented examples or placeholder validation as empirical evidence.

2026-07-04 -- Published the scaffold as public GitHub repository `BrettRey/lingputation-codebook-registry`. Reason: Brett asked to make the infrastructure public.

2026-07-04 -- Documented a license split: MIT for software, scripts, schemas, and interface code; CC BY 4.0 for codebook specifications, registry metadata, validation-record content, examples, and documentation unless a registry entry states otherwise. Reason: this is both software infrastructure and a scholarly registry/content format.

2026-07-04 -- Added `cgelbank-category-function-core` as the first real, non-toy registry package. Reason: CGELBank is a source-grounded annotation infrastructure precedent with a manual, validator, IAA study, category/function separation, and documented failure zones.

2026-07-04 -- Scoped the CGELBank package to core category/function/projection conventions rather than the full annotation manual. Reason: a first registry package should demonstrate the method without pretending to encode every CGELBank construction policy.
