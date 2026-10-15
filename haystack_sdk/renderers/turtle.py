"""Turtle (RDF) renderer for Brick Schema export; takes a class-resolver callback so the SDK stays decoupled from any Brick storage backend."""

from __future__ import annotations

import json
from typing import Any

from haystack_sdk.renderers._brick_graph import (
    BRICK_CLASS_TAG,
    DEFAULT_PREFIXES,
    ENTITY_PREFIX,
    NETIX_PREFIX,
    BrickNode,
    ResolveBrickClass,
    build_brick_nodes,
    compact,
    expand,
)
from haystack_sdk.renderers._brick_graph import markers_of as _markers
from haystack_sdk.renderers._brick_graph import strip_id as _strip_id

__all__ = [
    "BRICK_CLASS_TAG",
    "DEFAULT_PREFIXES",
    "ENTITY_PREFIX",
    "NETIX_PREFIX",
    "ResolveBrickClass",
    "_markers",
    "_strip_id",
    "render_turtle",
]


def render_turtle(
    tag_dicts: list[dict[str, Any]],
    resolve_class: ResolveBrickClass,
    *,
    extra_prefixes: dict[str, str] | None = None,
) -> str:
    """Render Haystack entity dicts (each needing an ``id`` key) as a Brick model in Turtle; see ``_brick_graph`` for
    how sites, spaces, equips and points become typed, related nodes.
    """
    prefixes = dict(DEFAULT_PREFIXES)
    if extra_prefixes:
        prefixes.update(extra_prefixes)

    lines = [f"@prefix {p}: <{uri}> ." for p, uri in prefixes.items()] + [""]
    for node in build_brick_nodes(tag_dicts, resolve_class, prefixes):
        lines.extend(_emit_node(node, prefixes))
    return "\n".join(lines) + "\n"


def _term(iri: str, prefixes: dict[str, str]) -> str:
    return compact(iri, prefixes) or f"<{iri}>"


def _emit_node(node: BrickNode, prefixes: dict[str, str]) -> list[str]:
    statements = ["a " + ", ".join(_term(cls, prefixes) for cls in node.types)]
    if node.label is not None:
        # A JSON string literal is also a valid Turtle STRING_LITERAL_QUOTE (same escapes, \uXXXX included).
        statements.append(f"rdfs:label {json.dumps(node.label, ensure_ascii=False)}")
    for predicate, target in node.relations:
        statements.append(f"{_term(expand(predicate, prefixes), prefixes)} {_term(target, prefixes)}")
    if node.suggested_class:
        statements.append(f"netix:suggestedClass {_term(node.suggested_class, prefixes)}")
    if node.confidence is not None:
        statements.append(f'netix:matchConfidence "{node.confidence:.2f}"^^xsd:decimal')

    block = [_term(node.iri, prefixes)]
    for i, statement in enumerate(statements):
        block.append(f"    {statement}{' ;' if i < len(statements) - 1 else ' .'}")
    block.append("")
    return block
