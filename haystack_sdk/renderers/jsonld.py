"""JSON-LD renderer for Brick Schema export; the same model as the Turtle renderer, so both parse to isomorphic graphs."""

from __future__ import annotations

from typing import Any

from haystack_sdk.renderers._brick_graph import (
    DEFAULT_PREFIXES,
    BrickNode,
    ResolveBrickClass,
    build_brick_nodes,
    compact,
    expand,
)


def render_jsonld(
    tag_dicts: list[dict[str, Any]],
    resolve_class: ResolveBrickClass,
    *,
    extra_context: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Render Haystack entity dicts as a JSON-LD ``@graph`` Brick model."""
    context: dict[str, str] = dict(DEFAULT_PREFIXES)
    if extra_context:
        context.update(extra_context)
    graph = [_node(node, context) for node in build_brick_nodes(tag_dicts, resolve_class, context)]
    return {"@context": context, "@graph": graph}


def _term(iri: str, context: dict[str, str]) -> str:
    return compact(iri, context) or iri


def _node(node: BrickNode, context: dict[str, str]) -> dict[str, Any]:
    types = [_term(cls, context) for cls in node.types]
    out: dict[str, Any] = {"@id": _term(node.iri, context), "@type": types[0] if len(types) == 1 else types}
    if node.label is not None:
        out["rdfs:label"] = node.label
    for predicate, target in node.relations:
        key = _term(expand(predicate, context), context)
        value = {"@id": _term(target, context)}
        existing = out.get(key)
        out[key] = value if existing is None else [*(existing if isinstance(existing, list) else [existing]), value]
    if node.suggested_class:
        out["netix:suggestedClass"] = {"@id": _term(node.suggested_class, context)}
    if node.confidence is not None:
        out["netix:matchConfidence"] = {"@value": f"{node.confidence:.2f}", "@type": "xsd:decimal"}
    return out
