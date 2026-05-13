"""Versioned Haystack 4 vocabulary packs.

Each pack is a frozen :class:`Vocabulary` of :class:`TagDef` records. Packs
are generated from JSON sources under ``haystack_sdk/vocabulary/data/``.

Use :func:`get_tag_def` for lookup by name across all packs, and
:func:`validate_markers` to verify that a marker set is known.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from haystack_sdk.vocabulary._base import TagDef, Vocabulary
from haystack_sdk.vocabulary.core import CORE
from haystack_sdk.vocabulary.district_cooling import DISTRICT_COOLING
from haystack_sdk.vocabulary.fdd import FDD
from haystack_sdk.vocabulary.healthcare import HEALTHCARE
from haystack_sdk.vocabulary.netix_custom import NETIX_CUSTOM
from haystack_sdk.vocabulary.residential import RESIDENTIAL
from haystack_sdk.vocabulary.retail_mall import RETAIL_MALL
from haystack_sdk.vocabulary.water_treatment import WATER_TREATMENT

__all__ = [
    "ALL_PACKS",
    "CORE",
    "DISTRICT_COOLING",
    "FDD",
    "HEALTHCARE",
    "NETIX_CUSTOM",
    "RESIDENTIAL",
    "RETAIL_MALL",
    "WATER_TREATMENT",
    "TagDef",
    "ValidationResult",
    "Vocabulary",
    "get_tag_def",
    "validate_markers",
]


ALL_PACKS: tuple[Vocabulary, ...] = (
    CORE,
    FDD,
    NETIX_CUSTOM,
    RETAIL_MALL,
    RESIDENTIAL,
    HEALTHCARE,
    WATER_TREATMENT,
    DISTRICT_COOLING,
)


def get_tag_def(name: str) -> TagDef | None:
    """Find a tag definition by name across all packs.

    Packs are searched in declaration order; the first match wins. Returns
    ``None`` if the tag is not in any pack.
    """
    for pack in ALL_PACKS:
        tag = pack.get(name)
        if tag is not None:
            return tag
    return None


@dataclass(frozen=True)
class ValidationResult:
    """Result of validating a set of marker/tag names against the SDK vocabulary."""

    known: frozenset[str] = field(default_factory=frozenset)
    unknown: frozenset[str] = field(default_factory=frozenset)

    @property
    def is_valid(self) -> bool:
        return not self.unknown


def validate_markers(names: set[str] | frozenset[str], *, extra: set[str] | None = None) -> ValidationResult:
    """Classify each name as known (present in any pack) or unknown.

    ``extra`` is an optional set of additional names to treat as known —
    e.g. per-org custom tags from a service-side store.
    """
    all_known = set()
    for pack in ALL_PACKS:
        all_known.update(pack.names())
    if extra:
        all_known.update(extra)

    names = set(names)
    return ValidationResult(
        known=frozenset(names & all_known),
        unknown=frozenset(names - all_known),
    )
