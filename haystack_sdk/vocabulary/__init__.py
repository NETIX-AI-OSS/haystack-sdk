"""Versioned Haystack 4 vocabulary packs; use :func:`get_tag_def` for cross-pack lookup and :func:`validate_markers` to check a marker set."""

from __future__ import annotations

from dataclasses import dataclass, field

from haystack_sdk.vocabulary._base import TagDef, Vocabulary
from haystack_sdk.vocabulary.core import PACK as CORE
from haystack_sdk.vocabulary.district_cooling import PACK as DISTRICT_COOLING
from haystack_sdk.vocabulary.fdd import PACK as FDD
from haystack_sdk.vocabulary.healthcare import PACK as HEALTHCARE
from haystack_sdk.vocabulary.netix_custom import PACK as NETIX_CUSTOM
from haystack_sdk.vocabulary.residential import PACK as RESIDENTIAL
from haystack_sdk.vocabulary.retail_mall import PACK as RETAIL_MALL
from haystack_sdk.vocabulary.water_treatment import PACK as WATER_TREATMENT

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
    """Find a tag definition by name across all packs, searched in declaration order (first match wins); ``None`` if not found."""
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
    """Classify each name as known (present in any pack) or unknown; ``extra`` adds names to treat as known, e.g. per-org custom tags."""
    all_known: set[str] = set()
    for pack in ALL_PACKS:
        all_known.update(pack.names())
    if extra:
        all_known.update(extra)

    names = set(names)
    return ValidationResult(
        known=frozenset(names & all_known),
        unknown=frozenset(names - all_known),
    )
