"""Brick Schema class registry + resolver; covers only universal *point*-level mappings — *equip*-level mappings live in asset-service's ``AssetClass.brick_class``."""

from __future__ import annotations

import json
from collections.abc import Iterator, Sequence
from dataclasses import dataclass
from importlib import resources
from typing import Any

__all__ = [
    "BRICK_PREFIX",
    "BRICK_VERSION",
    "BrickClass",
    "brick_class_kind",
    "find_brick_class",
    "iter_brick_classes",
    "jaccard_similarity",
    "normalize_brick_class",
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


def _read_json(name: str) -> Any:
    return json.loads(resources.files("haystack_sdk.brick.data").joinpath(name).read_text())


def _load_classes() -> tuple[BrickClass, ...]:
    entries = _read_json("brick_mappings.json")
    return tuple(
        BrickClass(
            name=e["name"],
            display_name=e["display_name"],
            haystack_tags=tuple(sorted(e["haystack_tags"])),
            brick_class=e["brick_class"],
        )
        for e in entries
    )


def _load_ontology_index() -> tuple[str, dict[str, str]]:
    # Generated from the Brick ontology by scripts/generate_brick_classes.py: local name -> kind.
    index = _read_json("brick_classes.json")
    return str(index["version"]), dict(index["classes"])


_CLASSES: tuple[BrickClass, ...] = _load_classes()
BRICK_VERSION, _ONTOLOGY_CLASSES = _load_ontology_index()


def iter_brick_classes() -> Iterator[BrickClass]:
    """Yield every registered :class:`BrickClass`."""
    return iter(_CLASSES)


def jaccard_similarity(a: Sequence[str], b: Sequence[str]) -> float:
    """Jaccard similarity (|A∩B| / |A∪B|) between two tag lists."""
    set_a, set_b = set(a), set(b)
    union = set_a | set_b
    return (len(set_a & set_b) / len(union)) if union else 0.0


def normalize_brick_class(value: str | None) -> str | None:
    """``brick:X``, bare ``X`` or the full Brick IRI as the ``brick:X`` qname, or None when *value* is not a class of the bundled Brick ontology."""
    if not value or not isinstance(value, str):
        return None
    local = value.strip()
    if local.startswith(BRICK_PREFIX):
        local = local[len(BRICK_PREFIX) :]
    elif local.startswith("brick:"):
        local = local[len("brick:") :]
    return f"brick:{local}" if local in _ONTOLOGY_CLASSES else None


def brick_class_kind(qname: str | None) -> str | None:
    """``point``, ``equipment``, ``location``, ``system``, ``collection`` or ``other`` for a Brick class, None when unknown."""
    normalized = normalize_brick_class(qname)
    return _ONTOLOGY_CLASSES[normalized[len("brick:") :]] if normalized else None


def _same_kind(markers: set[str], candidates: Sequence[BrickClass]) -> list[BrickClass]:
    # A point never resolves to an equipment class (or the reverse), however many markers they share.
    for kind in ("point", "equip"):
        if kind in markers:
            return [entry for entry in candidates if kind in entry.haystack_tags]
    return list(candidates)


def find_brick_class(
    markers: Sequence[str],
    *,
    extra: Sequence[BrickClass] = (),
    min_confidence: float = 0.5,
) -> tuple[str | None, float]:
    """Resolve markers to a Brick class.

    Confidence 1.0 is an exact marker match, or else the single most specific mapping whose markers are all present
    (so ``his``, ``cur``, ``writable`` and inherited equipment markers do not block a match). Otherwise the closest
    mapping by Jaccard similarity with its score, or ``(None, 0.0)`` below ``min_confidence``. ``extra`` injects
    org-specific mappings without global mutation.
    """
    marker_set = set(markers)
    sorted_markers = sorted(marker_set)
    candidates = _same_kind(marker_set, list(_CLASSES) + list(extra))

    for entry in candidates:
        if list(entry.haystack_tags) == sorted_markers:
            return entry.brick_class, 1.0

    covering = [entry for entry in candidates if set(entry.haystack_tags) <= marker_set]
    if covering:
        widest = max(len(entry.haystack_tags) for entry in covering)
        most_specific = {entry.brick_class for entry in covering if len(entry.haystack_tags) == widest}
        if len(most_specific) == 1:
            return most_specific.pop(), 1.0

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
    """Return True if *qname* is a class of the bundled Brick ontology (see ``BRICK_VERSION``); use the optional ``brickschema`` package for SHACL validation of a whole model."""
    return normalize_brick_class(qname) is not None
