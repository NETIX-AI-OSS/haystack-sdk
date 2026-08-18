"""Brick Schema class registry + resolver; covers only universal *point*-level mappings — *equip*-level mappings live in asset-service's ``AssetClass.brick_class``."""

from __future__ import annotations

import json
from collections.abc import Iterator, Sequence
from dataclasses import dataclass
from importlib import resources

__all__ = [
    "BRICK_PREFIX",
    "BrickClass",
    "find_brick_class",
    "iter_brick_classes",
    "jaccard_similarity",
    "validate_brick_class",
]


BRICK_PREFIX = "https://brickschema.org/schema/Brick#"


@dataclass(frozen=True, slots=True)
class BrickClass:
    """A Brick Schema class mapped from a Haystack marker combination."""

    name: str
    display_name: str
    haystack_tags: tuple[str, ...]
    brick_class: str


def _load_classes() -> tuple[BrickClass, ...]:
    raw = resources.files("haystack_sdk.brick.data").joinpath("brick_mappings.json").read_text()
    entries = json.loads(raw)
    return tuple(
        BrickClass(
            name=e["name"],
            display_name=e["display_name"],
            haystack_tags=tuple(sorted(e["haystack_tags"])),
            brick_class=e["brick_class"],
        )
        for e in entries
    )


_CLASSES: tuple[BrickClass, ...] = _load_classes()


def iter_brick_classes() -> Iterator[BrickClass]:
    """Yield every registered :class:`BrickClass`."""
    return iter(_CLASSES)


def jaccard_similarity(a: Sequence[str], b: Sequence[str]) -> float:
    """Jaccard similarity (|A∩B| / |A∪B|) between two tag lists."""
    set_a, set_b = set(a), set(b)
    union = set_a | set_b
    return (len(set_a & set_b) / len(union)) if union else 0.0


def find_brick_class(
    markers: Sequence[str],
    *,
    extra: Sequence[BrickClass] = (),
    min_confidence: float = 0.5,
) -> tuple[str | None, float]:
    """Resolve markers to a Brick class, returning ``(None, 0.0)`` below ``min_confidence``; ``extra`` injects org-specific mappings without global mutation."""
    sorted_markers = sorted(markers)
    candidates = list(_CLASSES) + list(extra)

    for entry in candidates:
        if list(entry.haystack_tags) == sorted_markers:
            return entry.brick_class, 1.0

    best: BrickClass | None = None
    best_score = 0.0
    for entry in candidates:
        score = jaccard_similarity(sorted_markers, entry.haystack_tags)
        if score > best_score:
            best_score = score
            best = entry

    if best is None or best_score < min_confidence:
        return None, 0.0
    return best.brick_class, best_score


def validate_brick_class(qname: str) -> bool:
    """Return True if *qname* is in the local registry; use the optional ``brickschema`` package for deep SHACL validation."""
    return any(entry.brick_class == qname for entry in _CLASSES)
