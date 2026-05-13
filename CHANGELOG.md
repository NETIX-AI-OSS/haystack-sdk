# Changelog

## v1.0.0 — initial release

Extracted Haystack 4 wire-format I/O, filter parser, vocabulary, and Brick mapping into a standalone, framework-agnostic Python package.

### Added

- Zinc, Trio, and Haystack 4 JSON parsers and renderers.
- Recursive-descent Haystack filter parser with full grammar support (AND/OR/NOT, paths, comparisons, refs).
- `Ref` parsing and normalization.
- Vocabulary packs as generated dataclasses:
  - `CORE` — Haystack 4 core (96 tags)
  - `FDD`, `NETIX_CUSTOM`, `RETAIL_MALL`, `RESIDENTIAL`, `HEALTHCARE`, `WATER_TREATMENT`, `DISTRICT_COOLING`
- Brick Schema class registry with optional `brickschema`-based validation.
- `scripts/generate_vocabulary.py` and `scripts/check_vocabulary_generated.py` for build-time validation.

### Migration notes

Replaces in-service modules previously at:
- `tag-service/tag/utils/haystack_parsers.py`
- `tag-service/tag/utils/haystack_renderers.py`
- `tag-service/tag/utils/haystack_filter.py`
- `tag-service/tag/utils/haystack_formats.py`
- `tag-service/tag/utils/haystack_brick.py` (mapping logic)
- `tag-service/tag/fixtures/{haystack_core,fdd,netix_custom,*}_tags.json`
- `tag-service/tag/fixtures/brick_mappings.json`

The DRF `BaseParser`/`BaseRenderer` adapters stay in services and call into the lib's pure functions.
