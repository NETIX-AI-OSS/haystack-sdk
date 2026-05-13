"""Zinc parser — Haystack 4 spec-compliant subset.

Parses the most common Zinc constructs used by NETIX services:
    - ``ver:"3.0"`` meta line
    - column header
    - Markers (``M``), Null (``N``), Bool (``T``/``F``)
    - Numbers (``42``, ``-3.14``, ``42 kW``)
    - Strings (``"hello"`` with escape sequences)
    - Refs (``@foo``, ``@foo "Display Name"``)

Edge cases not handled: nested grids, lists, dicts, multi-line records.
"""

from __future__ import annotations

import json
import re
from typing import Any

from haystack_sdk.types import Column, Grid


def parse_zinc(text: str) -> Grid:
    """Parse a Zinc-formatted grid into a :class:`Grid` dict."""
    text = text.strip()
    if not text:
        raise ValueError("Empty Zinc body")

    lines = text.split("\n")
    if len(lines) < 2:
        raise ValueError("Zinc body must have at least a meta line and a column header")

    meta = _parse_meta(lines[0])
    col_names = [c.strip() for c in lines[1].split(",")]
    cols: list[Column] = [{"name": name} for name in col_names]

    rows: list[dict[str, Any]] = []
    for line in lines[2:]:
        if not line.strip():
            continue
        rows.append(_parse_row(line, col_names))

    return {"meta": meta, "cols": cols, "rows": rows}


def _parse_meta(line: str) -> dict[str, Any]:
    meta: dict[str, Any] = {}
    ver_match = re.search(r'ver:"([^"]*)"', line)
    if ver_match:
        meta["ver"] = ver_match.group(1)
    return meta


def _parse_row(line: str, col_names: list[str]) -> dict[str, Any]:
    cells = _split_cells(line)
    row: dict[str, Any] = {}
    for i, name in enumerate(col_names):
        row[name] = _parse_val(cells[i].strip()) if i < len(cells) else None
    return row


def _split_cells(line: str) -> list[str]:
    cells: list[str] = []
    current: list[str] = []
    in_quote = False
    for ch in line:
        if ch == '"' and (not current or current[-1] != "\\"):
            in_quote = not in_quote
            current.append(ch)
        elif ch == "," and not in_quote:
            cells.append("".join(current))
            current = []
        else:
            current.append(ch)
    cells.append("".join(current))
    return cells


def _parse_number_or_str(val: str) -> Any:
    try:
        tok = val.split(" ")[0]
        return float(tok) if "." in tok else int(tok)
    except ValueError:
        return val


def _parse_val(val: str) -> Any:
    if not val or val == "N":
        return None
    if val == "M":
        return "m:"
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
