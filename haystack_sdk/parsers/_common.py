"""Shared parsing helpers used by both the Zinc and Trio parsers."""

from __future__ import annotations

import json
from typing import Any


def _parse_number_or_str(val: str) -> Any:
    """Try to parse *val* as an int or float; fall back to returning it as a string."""
    try:
        tok = val.split(" ")[0]
        return float(tok) if "." in tok else int(tok)
    except ValueError:
        return val


def _parse_val_common(
    val: str,
    *,
    empty_is_marker: bool,
    m_is_marker: bool,
) -> Any:
    """Parse a value token shared by Zinc and Trio; the two formats differ only in which sentinel maps to marker vs. None, via the two flags."""
    if not val:
        return "m:" if empty_is_marker else None
    if val == "M":
        return "m:" if m_is_marker else None
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
