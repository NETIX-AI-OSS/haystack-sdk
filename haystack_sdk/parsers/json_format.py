"""Haystack 4 JSON parser.

Input is standard JSON with a ``{meta, cols, rows}`` shape. Values may carry
type prefixes (``m:``, ``n:``, ``r:``, etc.) — they are preserved verbatim
because downstream callers usually want the typed form.
"""

from __future__ import annotations

import json
from typing import Any

from haystack_sdk.types import Grid


def parse_json(text: str) -> Grid:
    """Parse a Haystack 4 JSON grid into a :class:`Grid` dict."""
    if not text:
        raise ValueError("Empty JSON body")
    try:
        payload: dict[str, Any] = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON: {exc}") from exc

    if not isinstance(payload, dict):
        raise ValueError("Top-level JSON must be an object")

    meta = payload.get("meta") or {"ver": "3.0"}
    cols = payload.get("cols") or []
    rows = payload.get("rows") or []

    if not isinstance(meta, dict):
        raise ValueError("`meta` must be an object")
    if not isinstance(cols, list):
        raise ValueError("`cols` must be a list")
    if not isinstance(rows, list):
        raise ValueError("`rows` must be a list")

    return {"meta": meta, "cols": cols, "rows": rows}
