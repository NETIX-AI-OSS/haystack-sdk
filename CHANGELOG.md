# Changelog

## Unreleased

Tooling and packaging only; no public API change.

- Added explicit workflow permissions to CI (security hardening).
- Added a mypy pre-commit hook.
- Declared the project venv for pyright in `pyproject.toml`.
- Collapsed multi-line comments to single-line across the package.
- Cleaned up docs, license headers and docstrings.
- CI: migrated `ubuntu-latest` jobs to the `build-only` runner.

## v1.0.2 — 2026-06-23

> Reconstructed from git history on 2026-09-14; derived from commit subjects and diffs
> rather than written at release time.

### Fixed

- Turtle export emitted the `;`/`.` statement separator *after* the inline
  `# fuzzy match (NN)` note. A Turtle `#` comment runs to end of line, so the separator was
  swallowed and every fuzzy-matched point (confidence < 1.0) produced invalid RDF that failed
  `rdflib`/`brickschema` validation. The note is now emitted after the separator.

### Changed

- Platform audit pass: removed dead code, factored shared parser logic into
  `haystack_sdk/parsers/_common.py` (used by both the Zinc and Trio parsers), simplified the
  JSON-LD and Turtle renderers and the vocabulary base, and tidied
  `scripts/generate_vocabulary.py`.
- Expanded renderer, parser and round-trip test coverage, with new golden-grid fixtures.

## v1.0.1 — 2026-06-07

> Reconstructed from git history on 2026-09-14; derived from commit subjects and diffs
> rather than written at release time.

### Fixed

- Removed a redundant `force-include` that produced duplicate entries in the built wheel.

### Changed

- Pinned `hatchling==1.30.1` for reproducible source builds.

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
