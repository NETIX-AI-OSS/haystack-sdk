"""Zinc renderer."""

from __future__ import annotations

from typing import Any

from haystack_sdk.formats import zinc_encode_scalar


def render_zinc(grid: dict[str, Any]) -> str:
    """Render a grid dict (``{meta, cols, rows}``) as a Zinc string."""
    meta = grid.get("meta") or {}
    cols = grid.get("cols") or []
    rows = grid.get("rows") or []

    if not cols:
        return 'ver:"3.0"\nempty\n'

    meta_parts = ['ver:"3.0"']
    for k, v in sorted(meta.items()):
        if k == "ver":
            continue
        meta_parts.append(f"{k}:{zinc_encode_scalar(v)}")

    col_names = [c["name"] for c in cols]
    lines = [" ".join(meta_parts), ",".join(col_names)]

    for row in rows:
        cells = [zinc_encode_scalar(row.get(name)) for name in col_names]
        lines.append(",".join(cells))

    return "\n".join(lines) + "\n"


def tags_to_zinc(tag_dicts: list[dict[str, Any]], meta: dict[str, Any] | None = None) -> str:
    """Convert a list of tag dicts directly to a Zinc string.

    Convenience wrapper that builds a grid and renders it.
    """
    if not tag_dicts:
        return 'ver:"3.0"\nempty\n'

    col_names: set[str] = set()
    for d in tag_dicts:
        col_names.update(d.keys())

    cols = [{"name": n} for n in sorted(col_names)]
    rows = [{n: d.get(n) for n in sorted(col_names) if n in d} for d in tag_dicts]

    grid_meta = {"ver": "3.0"}
    if meta:
        grid_meta.update(meta)

    return render_zinc({"meta": grid_meta, "cols": cols, "rows": rows})
