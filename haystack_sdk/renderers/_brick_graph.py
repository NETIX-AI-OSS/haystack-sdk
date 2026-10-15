"""The Brick model the Turtle and JSON-LD renderers both serialize: one node per site, building, floor, space, equip and
point entity, related by ``brick:isPointOf`` / ``brick:hasLocation`` / ``brick:isPartOf``.

Entities are Haystack tag dicts. ``id`` names the node; markers (``"m:"`` values) give its kind; ``dis`` becomes its
``rdfs:label``; ``equipRef`` / ``spaceRef`` / ``floorRef`` / ``siteRef`` relate it to other entities; an optional
``brickClass`` (``brick:X``, ``X`` or the Brick IRI) pins an equip's or point's class, e.g. from an asset class. A
reference is emitted as given, so a caller that wants a closed model passes the referenced entities too.
"""

from __future__ import annotations

import re
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass, field
from typing import Any
from urllib.parse import quote

from haystack_sdk.brick import BRICK_PREFIX, brick_class_kind, normalize_brick_class

NETIX_PREFIX = "https://netix.ai/schema#"
ENTITY_PREFIX = "https://netix.ai/entity#"
REC_PREFIX = "https://w3id.org/rec#"
RDF_PREFIX = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
RDFS_PREFIX = "http://www.w3.org/2000/01/rdf-schema#"
XSD_PREFIX = "http://www.w3.org/2001/XMLSchema#"

# Shared by both renderers; ``bldg`` is the namespace entity ids are minted in.
DEFAULT_PREFIXES: dict[str, str] = {
    "brick": BRICK_PREFIX,
    "rec": REC_PREFIX,
    "netix": NETIX_PREFIX,
    "bldg": ENTITY_PREFIX,
    "rdf": RDF_PREFIX,
    "rdfs": RDFS_PREFIX,
    "xsd": XSD_PREFIX,
}

BRICK_CLASS_TAG = "brickClass"

# resolve_class returns (qname, confidence), or (None, 0.0) if unmapped.
ResolveBrickClass = Callable[[Sequence[str]], tuple[str | None, float]]

# Brick 1.4 deprecates brick:Site & co. for RealEstateCore classes, yet its own shapes still require brick:Location
# for hasLocation / isPointOf targets, so a location carries both.
_LOCATION_TYPES: dict[str, tuple[str, ...]] = {
    "site": ("rec:Site", "brick:Site"),
    "building": ("rec:Building", "brick:Building"),
    "floor": ("rec:Level", "brick:Floor"),
    "space": ("rec:Space", "brick:Space"),
}
# The refs a node may hang off, most specific first.
_LOCATION_REFS = ("spaceRef", "floorRef", "siteRef")
_LOCATION_PARENT_REFS: dict[str, tuple[str, ...]] = {
    "site": (),
    "building": ("siteRef",),
    "floor": ("siteRef",),
    "space": ("floorRef", "siteRef"),
}
_KIND_MARKERS = (
    ("point", "point"),
    ("equip", "equip"),
    ("device", "equip"),
    ("site", "site"),
    ("building", "building"),
    ("floor", "floor"),
    ("space", "space"),
)
_CLASS_KINDS = {"point": "point", "equipment": "equip"}
_GENERIC_POINT_CLASSES = (
    ("sensor", "brick:Sensor"),
    ("cmd", "brick:Command"),
    ("sp", "brick:Setpoint"),
    ("alarm", "brick:Alarm"),
)

# A Turtle PN_LOCAL we can write unescaped: no leading '-' / '.', no trailing '.'.
_SAFE_LOCAL = re.compile(r"[A-Za-z0-9_](?:[A-Za-z0-9_.-]*[A-Za-z0-9_-])?")


@dataclass
class BrickNode:
    """One subject of the model; every IRI held here is absolute."""

    iri: str
    types: list[str]
    label: str | None = None
    relations: list[tuple[str, str]] = field(default_factory=list)
    suggested_class: str | None = None
    confidence: float | None = None


def markers_of(entity: dict[str, Any]) -> list[str]:
    """The entity's marker tag names, sorted."""
    return sorted(k for k, v in entity.items() if v == "m:")


def strip_id(raw: str) -> str:
    """``r:@abc dis``, ``@abc`` and ``abc`` all name the local id ``abc``."""
    if raw.startswith("r:"):
        raw = raw[2:]
    if raw.startswith("@"):
        raw = raw[1:]
    return raw.split(" ", 1)[0]


def expand(qname: str, prefixes: dict[str, str]) -> str:
    """``brick:AHU`` → the full IRI; anything without a known prefix is returned unchanged."""
    prefix, sep, local = qname.partition(":")
    return prefixes[prefix] + local if sep and prefix in prefixes else qname


def compact(iri: str, prefixes: dict[str, str]) -> str | None:
    """The ``prefix:local`` form of *iri* when one is writable as-is in Turtle and JSON-LD, else None."""
    for prefix, namespace in sorted(prefixes.items(), key=lambda item: -len(item[1])):
        if iri.startswith(namespace) and _SAFE_LOCAL.fullmatch(iri[len(namespace) :]):
            return f"{prefix}:{iri[len(namespace):]}"
    return None


def _entity_iri(local: str, namespace: str) -> str:
    return namespace + (local if _SAFE_LOCAL.fullmatch(local) else quote(local, safe=""))


def _ref(entity: dict[str, Any], key: str, namespace: str) -> str | None:
    value = entity.get(key)
    if not isinstance(value, str) or not value:
        return None
    local = strip_id(value)
    return _entity_iri(local, namespace) if local else None


def _first_ref(entity: dict[str, Any], keys: Iterable[str], namespace: str) -> str | None:
    return next((iri for iri in (_ref(entity, key, namespace) for key in keys) if iri), None)


def _entity_kind(markers: Iterable[str], declared: str | None, resolved: str | None) -> str | None:
    marker_set = set(markers)
    for marker, kind in _KIND_MARKERS:
        if marker in marker_set:
            return kind
    # No kind marker: fall back to what the declared, else the resolved, Brick class is.
    for qname in (declared, resolved):
        class_kind = _CLASS_KINDS.get(brick_class_kind(qname) or "")
        if class_kind:
            return class_kind
    return None


def _generic_point_class(markers: Iterable[str]) -> str:
    marker_set = set(markers)
    return next((cls for marker, cls in _GENERIC_POINT_CLASSES if marker in marker_set), "brick:Point")


def _resolve(markers: list[str], resolve_class: ResolveBrickClass) -> tuple[str | None, float]:
    if not markers:
        return None, 0.0
    qname, confidence = resolve_class(markers)
    # A class the ontology does not define would type nothing a Brick tool understands.
    return normalize_brick_class(qname), confidence


def _point_node(
    node: BrickNode,
    entity: dict[str, Any],
    markers: list[str],
    declared: str | None,
    resolver_result: tuple[str | None, float],
    namespace: str,
) -> None:
    qname, confidence = resolver_result
    if declared and brick_class_kind(declared) == "point":
        node.types = [declared]
    elif qname and confidence >= 1.0 and brick_class_kind(qname) == "point":
        node.types = [qname]
    else:
        node.types = [_generic_point_class(markers)]
        if qname and brick_class_kind(qname) == "point" and qname != node.types[0]:
            node.suggested_class, node.confidence = qname, confidence
    target = _first_ref(entity, ("equipRef", *_LOCATION_REFS), namespace)
    if target:
        node.relations.append(("brick:isPointOf", target))


def _equip_node(
    node: BrickNode,
    entity: dict[str, Any],
    declared: str | None,
    resolver_result: tuple[str | None, float],
    namespace: str,
) -> None:
    qname, confidence = resolver_result
    if declared and brick_class_kind(declared) == "equipment":
        node.types = [declared]
    elif declared:
        # A Brick System / Collection (a chiller plant) has no equipment class, but is not one of its members either.
        node.types = ["brick:Equipment"]
    elif qname and confidence >= 1.0 and brick_class_kind(qname) == "equipment":
        node.types = [qname]
    else:
        node.types = ["brick:Equipment"]
    parent = _ref(entity, "equipRef", namespace)
    if parent:
        node.relations.append(("brick:isPartOf", parent))
    location = _first_ref(entity, _LOCATION_REFS, namespace)
    if location:
        node.relations.append(("brick:hasLocation", location))


def _location_node(node: BrickNode, entity: dict[str, Any], kind: str, declared: str | None, namespace: str) -> None:
    node.types = [declared] if declared and brick_class_kind(declared) == "location" else list(_LOCATION_TYPES[kind])
    parent = _first_ref(entity, _LOCATION_PARENT_REFS[kind], namespace)
    if parent:
        node.relations.append(("brick:isPartOf", parent))


def build_brick_nodes(
    entities: Iterable[dict[str, Any]], resolve_class: ResolveBrickClass, prefixes: dict[str, str]
) -> list[BrickNode]:
    """One node per entity whose kind can be told, in input order; a repeated id keeps its first entity."""
    namespace = prefixes["bldg"]
    nodes: list[BrickNode] = []
    seen: set[str] = set()
    for entity in entities:
        raw_id = entity.get("id")
        local = strip_id(str(raw_id)) if raw_id is not None else ""
        if not local:
            continue
        iri = _entity_iri(local, namespace)
        if iri in seen:
            continue
        markers = markers_of(entity)
        declared = normalize_brick_class(entity.get(BRICK_CLASS_TAG))
        resolved = _resolve(markers, resolve_class)
        kind = _entity_kind(markers, declared, resolved[0])
        if kind is None:
            continue
        dis = entity.get("dis")
        node = BrickNode(iri=iri, types=[], label=dis if isinstance(dis, str) and dis else None)
        if kind == "point":
            _point_node(node, entity, markers, declared, resolved, namespace)
        elif kind == "equip":
            _equip_node(node, entity, declared, resolved, namespace)
        else:
            _location_node(node, entity, kind, declared, namespace)
        # A node never relates to itself: the bug this model replaced emitted every point as isPointOf itself.
        node.relations = [(predicate, target) for predicate, target in node.relations if target != iri]
        node.types = [expand(qname, prefixes) for qname in node.types]
        if node.suggested_class:
            node.suggested_class = expand(node.suggested_class, prefixes)
        seen.add(iri)
        nodes.append(node)
    return nodes
