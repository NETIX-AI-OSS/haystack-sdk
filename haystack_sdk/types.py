"""Public type aliases used across the SDK."""

from __future__ import annotations

from typing import Any, TypedDict

# A Haystack value is one of:
#   - None (Null)
#   - bool
#   - int | float
#   - str  (plain string or type-prefixed: "m:", "n:42 kW", "r:abc Pump-1", "c:lat,lng", etc.)
HaystackValue = None | bool | int | float | str

# An entity is a dict of name → value.
HaystackEntity = dict[str, HaystackValue]


class Column(TypedDict):
    """Grid column metadata."""

    name: str


class Grid(TypedDict):
    """Haystack 4 grid: meta + columns + rows.

    The wire encoding uses ``ver:"3.0"`` because Project Haystack 4 retained
    the v3 grid format. See https://project-haystack.org/doc/docHaystack/Grids.
    """

    meta: dict[str, Any]
    cols: list[Column]
    rows: list[HaystackEntity]


# Marker sentinel — Haystack markers serialize to "m:" in JSON/Trio and to "M" in Zinc.
MARKER: str = "m:"
