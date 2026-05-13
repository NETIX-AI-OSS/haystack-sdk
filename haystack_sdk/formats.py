"""Scalar encoding helpers shared across renderers.

Used internally by the format-specific encoders in ``haystack_sdk.renderers``.
The public renderer surface lives in that subpackage; this module is kept
small and dependency-free.
"""

from __future__ import annotations

from typing import Any

_ZINC_ESCAPE = str.maketrans(
    {
        "\\": "\\\\",
        '"': '\\"',
        "\n": "\\n",
        "\r": "\\r",
        "\t": "\\t",
    }
)


def encode_scalar_json(value: Any) -> Any:
    """Encode a Python value as a Haystack 4 JSON scalar.

    Haystack 4 JSON uses type-prefixed strings for typed values:
        Marker  -> "m:"
        Bool    -> True / False  (native JSON)
        Number  -> "n:<val> [unit]"
        Str     -> "s:<val>"  (only when ambiguous; plain strings are fine)
        Ref     -> "r:<val> [dis]"
        Coord   -> "c:<lat>,<lng>"
    """
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return f"n:{value}"
    if isinstance(value, str):
        if value and len(value) >= 2 and value[1] == ":" and value[0] in "mnrstcxdu":
            return value
        return value
    return str(value)


def zinc_encode_str(value: str) -> str:
    """Encode a string into a Zinc-formatted cell value."""
    if value == "m:":
        return "M"
    if value.startswith("n:"):
        return value[2:]
    if value.startswith("c:"):
        return f"C({value[2:]})"
    if value.startswith("r:"):
        parts = value[2:].split(" ", 1)
        ref_id = parts[0]
        dis = parts[1] if len(parts) > 1 else ""
        return f'@{ref_id} "{dis.translate(_ZINC_ESCAPE)}"' if dis else f"@{ref_id}"
    return f'"{value.translate(_ZINC_ESCAPE)}"'


def zinc_encode_scalar(value: Any) -> str:
    """Encode any value as a Zinc cell."""
    if value is None:
        return "N"
    if isinstance(value, bool):
        return "T" if value else "F"
    if isinstance(value, (int, float)):
        return str(value)
    if not isinstance(value, str):
        return f'"{str(value).translate(_ZINC_ESCAPE)}"'
    return zinc_encode_str(value)


def trio_encode_str(value: str) -> str:
    """Encode a string into a Trio-formatted value (after ``key: ``)."""
    if value == "m:":
        return ""
    if value.startswith("r:"):
        return f"@{value[2:].split(' ', 1)[0]}"
    if value.startswith("n:"):
        return value[2:]
    return f'"{value.translate(_ZINC_ESCAPE)}"'


def trio_encode_scalar(value: Any) -> str:
    """Encode any value as a Trio scalar."""
    if value is None:
        return "N"
    if isinstance(value, bool):
        return "T" if value else "F"
    if isinstance(value, (int, float)):
        return str(value)
    if not isinstance(value, str):
        return f'"{str(value).translate(_ZINC_ESCAPE)}"'
    return trio_encode_str(value)
