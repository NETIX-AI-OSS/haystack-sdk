# Changelog

## v1.1.0 — Unreleased

### Fixed

- Brick export (`render_turtle` / `render_jsonld`) now emits a model rather than a flat list: distinct site, building,
  floor, space, equip and point nodes, points as `brick:isPointOf` their equip (or location), equips
  `brick:hasLocation` their space/floor/site, locations `brick:isPartOf` their parent. `siteRef` on a point is no
  longer rendered as `brick:isPartOf`, and a node is never related to itself.
- Unmapped or unconfident points are no longer dropped from the export, or typed with a guessed class: they are
  typed `brick:Point` / `Sensor` / `Command` / `Setpoint` / `Alarm` with `netix:suggestedClass` and
  `netix:matchConfidence`.
- `find_brick_class` no longer fails every historized point: the most specific mapping whose markers are all present
  scores 1.0, and points and equipment only resolve to their own kind.
- Four registry classes that do not exist in Brick 1.4 now map to ones that do: `Chilled_Water_Valve_Command` and
  `Hot_Water_Valve_Command` → `Valve_Position_Command`, `Fan_On_Off_Command` → `Start_Stop_Command`,
  `UPS` → `Electrical_Equipment`.

### Added

- `brickClass` entity tag to pin an equip's or point's Brick class (ignored unless it is a Brick 1.4 class of the
  right kind).
- `BRICK_VERSION`, `normalize_brick_class` and `brick_class_kind`, backed by an index of the Brick 1.4.4 ontology
  (`scripts/generate_brick_classes.py`). `validate_brick_class` now accepts any class of that ontology.
- A SHACL test that validates both exports against Brick 1.4 (`brickschema` joins the `dev` extra).

### Changed

- Entity IRIs move from `netix:<id>` to the `bldg:` namespace (`https://netix.ai/entity#`); `rec`, `rdfs` and `xsd`
  join the default prefixes. `netix:matchConfidence` is an `xsd:decimal` in both formats and the Turtle
  `# fuzzy match` comment is gone.

### Tooling

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
