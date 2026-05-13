"""haystack-sdk — Project Haystack 4 SDK.

Pure-Python, zero-runtime-dependency primitives for Haystack 4 wire formats,
filter expressions, vocabulary, and Brick Schema mapping.
"""

from __future__ import annotations

from haystack_sdk._version import __version__
from haystack_sdk.brick import (
    BRICK_PREFIX,
    BrickClass,
    find_brick_class,
    validate_brick_class,
)
from haystack_sdk.filter import (
    AndNode,
    CmpNode,
    FilterAST,
    FilterNode,
    MarkerNode,
    NotNode,
    OrNode,
    evaluate_filter,
    parse_filter,
)
from haystack_sdk.parsers import (
    ParseError,
    iter_entities,
    parse_grid,
    parse_json,
    parse_trio,
    parse_zinc,
)
from haystack_sdk.refs import (
    Ref,
    is_ref,
    normalize_ref,
    parse_ref,
)
from haystack_sdk.renderers import (
    render_grid,
    render_json,
    render_jsonld,
    render_trio,
    render_turtle,
    render_zinc,
    tags_to_json_grid,
    tags_to_trio,
    tags_to_zinc,
)
from haystack_sdk.types import MARKER, Column, Grid, HaystackEntity, HaystackValue
from haystack_sdk.vocabulary import (
    ALL_PACKS,
    CORE,
    DISTRICT_COOLING,
    FDD,
    HEALTHCARE,
    NETIX_CUSTOM,
    RESIDENTIAL,
    RETAIL_MALL,
    WATER_TREATMENT,
    TagDef,
    ValidationResult,
    Vocabulary,
    get_tag_def,
    validate_markers,
)

__all__ = [
    "ALL_PACKS",
    "BRICK_PREFIX",
    "CORE",
    "DISTRICT_COOLING",
    "FDD",
    "HEALTHCARE",
    "MARKER",
    "NETIX_CUSTOM",
    "RESIDENTIAL",
    "RETAIL_MALL",
    "WATER_TREATMENT",
    "AndNode",
    "BrickClass",
    "CmpNode",
    "Column",
    "FilterAST",
    "FilterNode",
    "Grid",
    "HaystackEntity",
    "HaystackValue",
    "MarkerNode",
    "NotNode",
    "OrNode",
    "ParseError",
    "Ref",
    "TagDef",
    "ValidationResult",
    "Vocabulary",
    "__version__",
    "evaluate_filter",
    "find_brick_class",
    "get_tag_def",
    "is_ref",
    "iter_entities",
    "normalize_ref",
    "parse_filter",
    "parse_grid",
    "parse_json",
    "parse_ref",
    "parse_trio",
    "parse_zinc",
    "render_grid",
    "render_json",
    "render_jsonld",
    "render_trio",
    "render_turtle",
    "render_zinc",
    "tags_to_json_grid",
    "tags_to_trio",
    "tags_to_zinc",
    "validate_brick_class",
    "validate_markers",
]
