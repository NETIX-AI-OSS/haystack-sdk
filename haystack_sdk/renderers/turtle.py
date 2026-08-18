"""Turtle (RDF) renderer for Brick Schema export; takes a class-resolver callback so the SDK stays decoupled from any Brick storage backend."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import Any

from haystack_sdk.brick import BRICK_PREFIX

NETIX_PREFIX = "https://netix.ai/schema#"

# Default prefix/context dict shared with the JSON-LD renderer.
DEFAULT_PREFIXES: dict[str, str] = {
    "brick": BRICK_PREFIX,
    "netix": NETIX_PREFIX,
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
}

# resolve_class returns (qname, confidence), or (None, 0.0) if unmapped.
ResolveBrickClass = Callable[[Sequence[str]], tuple[str | None, float]]


def render_turtle(
    tag_dicts: list[dict[str, Any]],
    resolve_class: ResolveBrickClass,
    *,
    extra_prefixes: dict[str, str] | None = None,
) -> str:
    """Render Haystack tag dicts (each needing an ``id`` key) to Turtle RDF, emitting ``rdf:type`` plus containment triples when refs are present."""
    prefixes = dict(DEFAULT_PREFIXES)
    if extra_prefixes:
        prefixes.update(extra_prefixes)

    lines = [f"@prefix {p}: <{uri}> ." for p, uri in prefixes.items()] + [""]

    for entity in tag_dicts:
        entity_id = entity.get("id")
        if entity_id is None:
            continue
        markers = _markers(entity)
        if not markers:
            continue
        brick_class, confidence = resolve_class(markers)
        if brick_class is None:
            continue
        lines.extend(_emit_entity(_strip_id(str(entity_id)), entity, brick_class, confidence))

    return "\n".join(lines) + "\n"


def _markers(entity: dict[str, Any]) -> list[str]:
    return sorted(k for k, v in entity.items() if v == "m:")


def _strip_id(raw: str) -> str:
    if raw.startswith("r:"):
        raw = raw[2:]
    if raw.startswith("@"):
        raw = raw[1:]
    return raw.split(" ", 1)[0]


def _emit_entity(entity_id: str, entity: dict[str, Any], brick_class: str, confidence: float) -> list[str]:
    # Fuzzy-match note must follow ';'/'.'; '#' comments run to end-of-line.
    type_comment = "" if confidence >= 1.0 else f"  # fuzzy match ({confidence:.2f})"
    triples = [f"    a {brick_class}"]

    for ref_key, brick_predicate in (("equipRef", "brick:isPointOf"), ("siteRef", "brick:isPartOf")):
        ref_val = entity.get(ref_key)
        if ref_val and isinstance(ref_val, str):
            stripped = _strip_id(ref_val)
            triples.append(f"    {brick_predicate} netix:{stripped}")

    block = [f"netix:{entity_id}"]
    for i, triple in enumerate(triples):
        sep = " ;" if i < len(triples) - 1 else " ."
        comment = type_comment if i == 0 else ""
        block.append(f"{triple}{sep}{comment}")
    block.append("")
    return block
