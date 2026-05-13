"""JSON-LD renderer for Brick Schema export."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import Any

from haystack_sdk.renderers.turtle import BRICK_PREFIX, NETIX_PREFIX, _strip_id  # internal reuse

ResolveBrickClass = Callable[[Sequence[str]], tuple[str | None, float]]


def render_jsonld(
    tag_dicts: list[dict[str, Any]],
    resolve_class: ResolveBrickClass,
    *,
    extra_context: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Render Haystack tag dicts as a JSON-LD ``@graph``."""
    context: dict[str, str] = {
        "brick": BRICK_PREFIX,
        "netix": NETIX_PREFIX,
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    }
    if extra_context:
        context.update(extra_context)

    graph: list[dict[str, Any]] = []
    for entity in tag_dicts:
        entity_id = entity.get("id")
        if entity_id is None:
            continue
        markers = sorted(k for k, v in entity.items() if v == "m:")
        if not markers:
            continue
        brick_class, confidence = resolve_class(markers)
        if brick_class is None:
            continue

        node: dict[str, Any] = {
            "@id": f"netix:{_strip_id(str(entity_id))}",
            "@type": brick_class,
        }
        for ref_key, ld_predicate in (("equipRef", "brick:isPointOf"), ("siteRef", "brick:isPartOf")):
            ref_val = entity.get(ref_key)
            if ref_val and isinstance(ref_val, str):
                node[ld_predicate] = {"@id": f"netix:{_strip_id(ref_val)}"}
        if confidence < 1.0:
            node["netix:matchConfidence"] = confidence

        graph.append(node)

    return {"@context": context, "@graph": graph}
