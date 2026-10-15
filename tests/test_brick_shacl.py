"""The Turtle and JSON-LD Brick exports validate against the Brick 1.4 SHACL shapes and describe the same graph."""

from __future__ import annotations

import json
from functools import cache
from importlib import resources

import pyshacl
import pytest
import rdflib
from rdflib.compare import isomorphic

from haystack_sdk import BRICK_VERSION, find_brick_class, render_jsonld, render_turtle

SH = rdflib.Namespace("http://www.w3.org/ns/shacl#")
BRICK = rdflib.Namespace("https://brickschema.org/schema/Brick#")
BLDG = rdflib.Namespace("https://netix.ai/entity#")

MODEL = [
    {"id": "r:@site-1 HQ", "site": "m:", "dis": "HQ"},
    {"id": "@building-2", "building": "m:", "siteRef": "@site-1", "dis": "Tower A"},
    {"id": "@floor-3", "floor": "m:", "siteRef": "@building-2", "dis": "Level 3"},
    {"id": "@space-4", "space": "m:", "floorRef": "@floor-3", "siteRef": "@building-2", "dis": "Plant room"},
    {
        "id": "@equip-5",
        "equip": "m:",
        "ahu": "m:",
        "air": "m:",
        "spaceRef": "@space-4",
        "siteRef": "@building-2",
        "dis": "AHU-5",
        "brickClass": "brick:Air_Handler_Unit",
    },
    # An asset class whose brick_class is not a Brick 1.4 class: the equip still gets a valid type.
    {"id": "@equip-6", "equip": "m:", "pump": "m:", "water": "m:", "equipRef": "@equip-5", "brickClass": "Sump_Pump"},
    # Two points on one equip, carrying the markers tag-service layers in (his, cur, the AHU's own markers).
    {
        "id": "@point-10",
        "point": "m:",
        "sensor": "m:",
        "air": "m:",
        "temp": "m:",
        "supply": "m:",
        "his": "m:",
        "cur": "m:",
        "equip": "m:",
        "ahu": "m:",
        "equipRef": "@equip-5",
        "dis": "AHU-5 supply air temp",
    },
    {"id": "@point-11", "point": "m:", "cmd": "m:", "fan": "m:", "speed": "m:", "his": "m:", "equipRef": "@equip-5"},
    {
        "id": "@point-12",
        "point": "m:",
        "sensor": "m:",
        "temp": "m:",
        "water": "m:",
        "his": "m:",
        "equipRef": "@equip-6",
    },
    {"id": "@point-13", "point": "m:", "his": "m:", "equipRef": "@equip-6"},
    # A point with no equip hangs off its most specific location.
    {
        "id": "@point-14",
        "point": "m:",
        "sensor": "m:",
        "air": "m:",
        "temp": "m:",
        "outside": "m:",
        "siteRef": "@site-1",
    },
]


@cache
def _brick() -> rdflib.Graph:
    ontology = resources.files("brickschema") / "ontologies" / "1.4" / "Brick.ttl"
    graph = rdflib.Graph()
    graph.parse(data=ontology.read_text(), format="turtle")
    return graph


def _violations(data: rdflib.Graph) -> list[tuple[str, str]]:
    """Violations whose focus node is ours; the bundled ontology trips a few shapes on its own terms."""
    ours = set(data.subjects())
    _, results, _ = pyshacl.validate(
        data, shacl_graph=_brick(), ont_graph=_brick(), inference="rdfs", advanced=True, allow_warnings=True
    )
    return sorted(
        (str(results.value(r, SH.focusNode)), str(results.value(r, SH.resultMessage)))
        for r in results.subjects(rdflib.RDF.type, SH.ValidationResult)
        if results.value(r, SH.focusNode) in ours and results.value(r, SH.resultSeverity) == SH.Violation
    )


def _turtle_graph() -> rdflib.Graph:
    return rdflib.Graph().parse(data=render_turtle(MODEL, find_brick_class), format="turtle")


def test_bundled_index_matches_the_ontology_version() -> None:
    assert BRICK_VERSION.startswith("1.4")


def test_turtle_and_jsonld_are_the_same_graph() -> None:
    jsonld = rdflib.Graph().parse(data=json.dumps(render_jsonld(MODEL, find_brick_class)), format="json-ld")
    assert isomorphic(_turtle_graph(), jsonld)


def test_model_has_distinct_point_equip_and_location_nodes() -> None:
    graph = _turtle_graph()
    assert (BLDG["point-10"], BRICK.isPointOf, BLDG["equip-5"]) in graph
    assert (BLDG["point-11"], BRICK.isPointOf, BLDG["equip-5"]) in graph
    assert (BLDG["point-10"], rdflib.RDF.type, BRICK.Supply_Air_Temperature_Sensor) in graph
    assert (BLDG["point-11"], rdflib.RDF.type, BRICK.Fan_Speed_Command) in graph
    assert (BLDG["equip-5"], rdflib.RDF.type, BRICK.Air_Handler_Unit) in graph
    assert (BLDG["equip-5"], BRICK.hasLocation, BLDG["space-4"]) in graph
    assert (BLDG["equip-6"], rdflib.RDF.type, BRICK.Pump) in graph
    assert (BLDG["equip-6"], BRICK.isPartOf, BLDG["equip-5"]) in graph
    assert (BLDG["floor-3"], BRICK.isPartOf, BLDG["building-2"]) in graph
    assert (BLDG["point-14"], BRICK.isPointOf, BLDG["site-1"]) in graph
    assert not any(s == o for s, _, o in graph.triples((None, BRICK.isPointOf, None)))


@pytest.mark.parametrize("fmt", ["turtle", "json-ld"])
def test_export_conforms_to_brick_shapes(fmt: str) -> None:
    if fmt == "turtle":
        data = _turtle_graph()
    else:
        data = rdflib.Graph().parse(data=json.dumps(render_jsonld(MODEL, find_brick_class)), format="json-ld")
    assert _violations(data) == []


def test_validation_catches_a_point_of_itself() -> None:
    # The pre-1.1 export: point subject and equipRef were the same asset id, so every point was a point of itself.
    legacy = """
    @prefix brick: <https://brickschema.org/schema/Brick#> .
    @prefix netix: <https://netix.ai/schema#> .
    netix:7 a brick:Air_Temperature_Sensor ; brick:isPointOf netix:7 .
    """
    violations = _violations(rdflib.Graph().parse(data=legacy, format="turtle"))
    assert any("Point of Equipment" in message for _, message in violations)
