"""Trio parser — record-separated key:value blocks.

Each entity is separated by ``\\n---\\n``. Within a block, each line is either:

    - ``key: value``
    - bare ``key`` (interpreted as a marker, value ``"m:"``)
    - comment (``// ...``) or blank line (skipped)
"""

from __future__ import annotations

import json
import re
from typing import Any

from haystack_sdk.types import Column, Grid


def parse_trio(text: str) -> Grid:
    """Parse a Trio-formatted document into a :class:`Grid` dict."""
    text = text.strip()
    if not text:
        raise ValueError("Empty Trio body")

    blocks = re.split(r"\n---\n", text)
    rows: list[dict[str, Any]] = []
    all_keys: set[str] = set()

    for block in blocks:
        row = _parse_block(block)
        if row:
            rows.append(row)
            all_keys.update(row.keys())

    cols: list[Column] = [{"name": k} for k in sorted(all_keys)]
    return {"meta": {"ver": "3.0"}, "cols": cols, "rows": rows}


def _parse_block(block: str) -> dict[str, Any]:
    row: dict[str, Any] = {}
    for raw_line in block.strip().split("\n"):
        line = raw_line.strip()
        if not line or line.startswith("//"):
            continue
        if ":" in line:
            key, _, val = line.partition(":")
            row[key.strip()] = _parse_val(val.strip())
        else:
            row[line.strip()] = "m:"
    return row


def _parse_number_or_str(val: str) -> Any:
    try:
        tok = val.split(" ")[0]
        return float(tok) if "." in tok else int(tok)
    except ValueError:
        return val


def _parse_val(val: str) -> Any:
    if not val or val == "M":
        return "m:"
    if val == "N":
        return None
    if val in ("T", "true", "F", "false"):
        return val in ("T", "true")
    if val.startswith("@"):
        return f"r:{val[1:]}"
    if val.startswith('"') and val.endswith('"'):
        try:
            return json.loads(val)
        except json.JSONDecodeError:
            return val[1:-1]
    return _parse_number_or_str(val)
