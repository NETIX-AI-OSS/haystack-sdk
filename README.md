# haystack-sdk

Project Haystack 4 SDK for NETIX services. Pure-Python parsers, renderers, vocabulary, and Brick Schema mapping. Zero runtime dependencies.

## Features

- **Wire-format I/O** for Zinc, Trio, and Haystack 4 JSON (parse + render).
- **Filter expressions** with full Haystack 4 grammar (AND/OR/NOT, paths, comparisons, refs).
- **Versioned vocabulary** for core Haystack 4 + NETIX domain packs (FDD, retail, residential, healthcare, water treatment, district cooling).
- **Brick Schema** class registry and validation.
- **Ref parsing and normalization** following the Haystack 4 spec.

The SDK is **framework-agnostic** — no Django, no DRF, no I/O dependencies. Services wrap these primitives in DRF parsers/renderers as needed.

## Installation

```toml
# pyproject.toml
[tool.uv.sources]
haystack-sdk = { git = "ssh://git@github.com/NETIX-AI-OSS/haystack-sdk.git", tag = "v1.0" }
```

For local development:

```toml
[tool.uv.sources]
haystack-sdk = { path = "../haystack-sdk" }
```

## Quick start

```python
from haystack_sdk import parse_grid, render_grid, parse_filter
from haystack_sdk.vocabulary import CORE, get_tag_def, validate_markers

# Parse Zinc into a grid dict
grid = parse_grid(zinc_text, format="zinc")

# Render to any format
output = render_grid(grid, format="trio")

# Filter
ast = parse_filter("equip and ahu")
matches = [r for r in grid["rows"] if ast.evaluate(r)]

# Vocabulary lookup
ahu_def = get_tag_def("ahu")              # TagDef(name="ahu", kind="Marker", ...)
validate_markers({"site", "ahu", "fooo"}) # → {"unknown": {"fooo"}, ...}
```

## Vocabulary

Core Haystack 4 vocabulary plus NETIX domain extension packs:

| Pack | Domain |
|---|---|
| `CORE` | Haystack 4 core tags (96 markers/kinds). |
| `FDD` | Fault detection & diagnostics — `equipType`, `faultType`, ...  |
| `NETIX_CUSTOM` | NETIX-specific custom tags. |
| `RETAIL_MALL` | Retail / mall building markers. |
| `RESIDENTIAL` | Smart residential markers. |
| `HEALTHCARE` | Healthcare-facility markers. |
| `WATER_TREATMENT` | Water-treatment plant markers. |
| `DISTRICT_COOLING` | District-cooling plant markers. |

Vocabulary `.py` files are generated from JSON sources under `haystack_sdk/vocabulary/data/`. Regenerate with:

```bash
python scripts/generate_vocabulary.py
```

The CI pipeline enforces that the generated files match their JSON sources.

## Versioning

Semver. v1.0 is the first stable release. The wire-format parsers and the vocabulary content are considered the stable contract.

## License

Apache-2.0
