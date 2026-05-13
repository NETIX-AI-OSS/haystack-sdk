"""Haystack 4 JSON renderer."""

from __future__ import annotations

import json
from typing import Any

from haystack_sdk.formats import encode_scalar_json


def render_json(grid: dict[str, Any]) -> str:
    """Render a grid dict as a Haystack 4 JSON string (compact)."""
    payload = _encode_grid(grid)
    return json.dumps(payload, separators=(",", ":"))


def tags_to_json_grid(tag_dicts: list[dict[str, Any]], meta: dict[str, Any] | None = None) -> dict[str, Any]:
    """Convert a list of tag dicts into a Haystack 4 JSON-shaped grid dict.

    Does not serialise — returns the Python object. Useful when the caller
    will JSON-encode it via DRF, FastAPI, etc.
    """
    if not tag_dicts:
        return {"meta": {"ver": "3.0"}, "cols": [], "rows": []}

    col_names: set[str] = set()
    for d in tag_dicts:
        col_names.update(d.keys())
    col_names_sorted = sorted(col_names)

    cols = [{"name": n} for n in col_names_sorted]
    rows: list[dict[str, Any]] = []
    for d in tag_dicts:
        row: dict[str, Any] = {}
        for name in col_names_sorted:
            if name in d:
                row[name] = encode_scalar_json(d[name])
        rows.append(row)

    grid_meta = {"ver": "3.0"}
    if meta:
        grid_meta.update(meta)

    return {"meta": grid_meta, "cols": cols, "rows": rows}


def _encode_grid(grid: dict[str, Any]) -> dict[str, Any]:
    meta = grid.get("meta") or {"ver": "3.0"}
    cols = grid.get("cols") or []
    rows = grid.get("rows") or []
    encoded_rows = [{k: encode_scalar_json(v) for k, v in row.items() if v is not None} for row in rows]
    return {"meta": meta, "cols": cols, "rows": encoded_rows}
