"""Base types for the vocabulary system.

Vocabulary packs are sets of :class:`TagDef` records describing Haystack 4
tags (markers, kinds, namespaces). Each pack is a frozen :class:`Vocabulary`.

Packs are generated from JSON sources under ``haystack_sdk/vocabulary/data/``
via ``scripts/generate_vocabulary.py`` — do not hand-edit the generated
``.py`` files.
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, field

_KIND_NAMES = {
    0: "Marker",
    1: "Bool",
    2: "Number",
    3: "Str",
    4: "Ref",
    5: "Uri",
    6: "Date",
    7: "Time",
    8: "DateTime",
    9: "Coord",
    10: "XStr",
}


@dataclass(frozen=True, slots=True)
class TagDef:
    """A single tag definition.

    Mirrors the previous ``HaystackTagDef`` Django model but is frozen and
    serializable. ``kind`` is the integer code (0=Marker, 1=Bool, ...) for
    wire compatibility with the legacy Django storage.
    """

    name: str
    display_name: str
    kind: int  # Use kind_name() for the human-readable label
    namespace: str = "phIoT"
    doc: str = ""
    supertype: str | None = None
    unit_quantity: str | None = None

    def kind_name(self) -> str:
        return _KIND_NAMES.get(self.kind, "Unknown")

    @property
    def is_marker(self) -> bool:
        return self.kind == 0


@dataclass(frozen=True)
class Vocabulary:
    """A named collection of :class:`TagDef` records."""

    name: str
    version: str
    tags: tuple[TagDef, ...] = field(default_factory=tuple)

    def __iter__(self) -> Iterator[TagDef]:
        return iter(self.tags)

    def __len__(self) -> int:
        return len(self.tags)

    def __contains__(self, name: object) -> bool:
        if not isinstance(name, str):
            return False
        return any(t.name == name for t in self.tags)

    def get(self, name: str) -> TagDef | None:
        for tag in self.tags:
            if tag.name == name:
                return tag
        return None

    def names(self) -> frozenset[str]:
        return frozenset(t.name for t in self.tags)
