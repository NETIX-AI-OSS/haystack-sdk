"""Wire-format renderers — Zinc, Trio, Haystack 4 JSON, Turtle, JSON-LD."""

from __future__ import annotations

from typing import Any

from haystack_sdk.renderers.json_format import render_json, tags_to_json_grid
from haystack_sdk.renderers.jsonld import render_jsonld
from haystack_sdk.renderers.trio import render_trio, tags_to_trio
from haystack_sdk.renderers.turtle import render_turtle
from haystack_sdk.renderers.zinc import render_zinc, tags_to_zinc

__all__ = [
    "render_grid",
    "render_json",
    "render_jsonld",
    "render_trio",
    "render_turtle",
    "render_zinc",
    "tags_to_json_grid",
    "tags_to_trio",
    "tags_to_zinc",
]


def render_grid(grid: dict[str, Any], *, format: str) -> str:
    """Render a grid in the requested wire format.

    ``format`` ∈ ``{"zinc", "trio", "json"}``.
    """
    if format == "zinc":
        return render_zinc(grid)
    if format == "trio":
        return render_trio(grid)
    if format == "json":
        return render_json(grid)
    raise ValueError(f"Unknown render format: {format!r}")
