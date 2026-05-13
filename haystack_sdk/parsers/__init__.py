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
    """Stream parsed entities one at a time.

    For very large grids, prefer this over :func:`parse_grid` to avoid
    materialising every row in memory at once. The Zinc and Trio parsers
    yield rows incrementally; the JSON parser falls back to a buffered parse
    and then yields, since JSON lacks a record separator.
    """
    grid = parse_grid(text, format=format)
    yield from grid["rows"]
