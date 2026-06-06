"""Wire-format parsers — Zinc, Trio, and Haystack 4 JSON.

All parsers return a :class:`haystack_sdk.types.Grid` dict.
"""

from __future__ import annotations

from collections.abc import Iterator

from haystack_sdk.parsers.json_format import parse_json
from haystack_sdk.parsers.trio import parse_trio
from haystack_sdk.parsers.zinc import parse_zinc
from haystack_sdk.types import Grid, HaystackEntity

__all__ = [
    "ParseError",
    "iter_entities",
    "parse_grid",
    "parse_json",
    "parse_trio",
    "parse_zinc",
]


class ParseError(ValueError):
    """Raised when wire input cannot be parsed."""


def parse_grid(text: str, *, format: str) -> Grid:
    """Dispatch parse based on ``format``.

    ``format`` must be one of ``"zinc"``, ``"trio"``, or ``"json"``.
    """
    if format == "zinc":
        return parse_zinc(text)
    if format == "trio":
        return parse_trio(text)
    if format == "json":
        return parse_json(text)
    raise ParseError(f"Unknown format: {format!r}")


def iter_entities(text: str, *, format: str) -> Iterator[HaystackEntity]:
    """Iterate over parsed entities from a wire-format document.

    Convenience wrapper around :func:`parse_grid` that yields each row dict
    individually. The full grid is buffered in memory before iteration begins —
    all three wire formats (Zinc, Trio, JSON) are fully parsed upfront.

    ``format`` must be one of ``"zinc"``, ``"trio"``, or ``"json"``.
    """
    grid = parse_grid(text, format=format)
    yield from grid["rows"]
