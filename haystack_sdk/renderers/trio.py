"""Trio renderer."""

from __future__ import annotations

from typing import Any

from haystack_sdk.formats import trio_encode_scalar


def render_trio(grid: dict[str, Any]) -> str:
    """Render a grid dict as a Trio string."""
    if not isinstance(grid, dict):
        return str(grid)

    rows = grid.get("rows") or []
    cols = grid.get("cols") or []
    col_names: list[str] = [c["name"] for c in cols] if cols else []

    blocks: list[str] = []
    for row in rows:
        lines: list[str] = []
        keys = col_names or sorted(row.keys())
        for key in keys:
            val = row.get(key)
            if val is None:
                continue
            if isinstance(val, str) and val == "m:":
                lines.append(key)
            else:
                lines.append(f"{key}: {trio_encode_scalar(val)}")
        blocks.append("\n".join(lines))

    return "\n---\n".join(blocks) + "\n"


def tags_to_trio(tag_dicts: list[dict[str, Any]]) -> str:
    """Convert a list of tag dicts directly to a Trio string."""
    blocks: list[str] = []
    for d in tag_dicts:
        lines: list[str] = []
        for key in sorted(d.keys()):
            val = d[key]
            if val == "m:":
                lines.append(key)
            else:
                lines.append(f"{key}: {trio_encode_scalar(val)}")
        blocks.append("\n".join(lines))
    return "\n---\n".join(blocks) + "\n"
