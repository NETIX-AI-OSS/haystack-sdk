"""Public type aliases used across the SDK."""

from __future__ import annotations

from typing import Any, TypedDict

# A Haystack value: None, bool, int|float, or str (optionally type-prefixed).
HaystackValue = None | bool | int | float | str

# An entity is a dict of name → value.
HaystackEntity = dict[str, HaystackValue]


class Column(TypedDict):
    """Grid column metadata."""

    name: str


class Grid(TypedDict):
    """Haystack 4 grid (meta + columns + rows); wire encoding uses ``ver:"3.0"`` since Haystack 4 retained the v3 grid format."""

    meta: dict[str, Any]
    cols: list[Column]
    rows: list[HaystackEntity]


# Marker sentinel — Haystack markers serialize to "m:" in JSON/Trio and to "M" in Zinc.
MARKER: str = "m:"
