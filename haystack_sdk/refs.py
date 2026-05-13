"""Haystack Ref parsing and validation.

A Ref is an identifier prefixed with ``@``. Format::

    @<id> [<dis>]

Where ``<id>`` is alphanumeric + ``_.-:`` and ``<dis>`` is an optional display
string. In the typed JSON form refs serialize as ``r:<id> [dis]``.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

_REF_ID_PATTERN = re.compile(r"^[A-Za-z0-9_.\-:~]+$")


@dataclass(frozen=True, slots=True)
class Ref:
    """A parsed Haystack reference."""

    id: str
    dis: str | None = None

    def __post_init__(self) -> None:
        if not self.id:
            raise ValueError("Ref id cannot be empty")
        if not _REF_ID_PATTERN.match(self.id):
            raise ValueError(f"Invalid ref id: {self.id!r}")

    def to_zinc(self) -> str:
        return f'@{self.id} "{self.dis}"' if self.dis else f"@{self.id}"

    def to_json(self) -> str:
        return f"r:{self.id} {self.dis}" if self.dis else f"r:{self.id}"

    def to_trio(self) -> str:
        return f"@{self.id}"


def parse_ref(value: str) -> Ref:
    """Parse a Haystack ref from any wire encoding.

    Accepts::

        "@abc"               → Ref(id="abc")
        "@abc Pump-1"        → Ref(id="abc", dis="Pump-1")
        '@abc "Pump-1"'      → Ref(id="abc", dis="Pump-1")
        "r:abc"              → Ref(id="abc")
        "r:abc Pump-1"       → Ref(id="abc", dis="Pump-1")
    """
    raw = value.strip()
    if raw.startswith("r:"):
        body = raw[2:]
    elif raw.startswith("@"):
        body = raw[1:]
    else:
        raise ValueError(f"Not a ref: {value!r}")

    parts = body.split(" ", 1)
    ref_id = parts[0]
    dis: str | None = None
    if len(parts) == 2:
        dis_raw = parts[1].strip()
        if dis_raw.startswith('"') and dis_raw.endswith('"'):
            dis_raw = dis_raw[1:-1]
        dis = dis_raw or None
    return Ref(id=ref_id, dis=dis)


def is_ref(value: object) -> bool:
    """Return True if *value* is a string-encoded ref ("@..." or "r:...")."""
    if not isinstance(value, str):
        return False
    return value.startswith("@") or value.startswith("r:")


def normalize_ref(value: str) -> str:
    """Normalize any ref encoding to the typed-JSON form (``r:<id>``)."""
    return parse_ref(value).to_json()
