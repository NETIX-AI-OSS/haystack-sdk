"""Renderer tests — Zinc, Trio, JSON, Turtle, JSON-LD."""

from __future__ import annotations

import json

import pytest

from haystack_sdk import (
    parse_zinc,
    render_grid,
    render_json,
    render_jsonld,
    render_trio,
    render_turtle,
    render_zinc,
    tags_to_json_grid,
    tags_to_trio,
    tags_to_zinc,
)
from haystack_sdk.formats import encode_scalar_json, trio_encode_scalar, zinc_encode_scalar

SAMPLE_GRID = {
    "meta": {"ver": "3.0"},
    "cols": [{"name": "id"}, {"name": "site"}, {"name": "dis"}],
    "rows": [
        {"id": "r:1", "site": "m:", "dis": "Main"},
        {"id": "r:2", "site": "m:", "dis": "Annex"},
    ],
}


class TestZincRenderer:
    def test_round_trip(self) -> None:
        zinc = render_zinc(SAMPLE_GRID)
        parsed = parse_zinc(zinc)
        assert parsed["rows"] == SAMPLE_GRID["rows"]

    def test_empty_grid(self) -> None:
        out = render_zinc({"meta": {"ver": "3.0"}, "cols": [], "rows": []})
        assert "empty" in out


class TestTrioRenderer:
    def test_markers_bare_keys(self) -> None:
        out = render_trio(SAMPLE_GRID)
        assert "site\n" in out  # marker rendered as bare key
        assert 'dis: "Main"' in out


class TestJsonRenderer:
    def test_round_trip(self) -> None:
        out = render_json(SAMPLE_GRID)
        payload = json.loads(out)
        assert payload["meta"]["ver"] == "3.0"
        assert len(payload["rows"]) == 2


class TestRenderGridDispatch:
    def test_unknown_format(self) -> None:
        with pytest.raises(ValueError):
            render_grid(SAMPLE_GRID, format="yaml")


SITE = {"id": "r:@site-1 HQ", "site": "m:", "dis": "HQ"}
AHU = {"id": "@equip-7", "equip": "m:", "ahu": "m:", "air": "m:", "siteRef": "@site-1", "dis": "AHU-7"}
POINT_A = {"id": "r:41", "point": "m:", "sensor": "m:", "air": "m:", "temp": "m:", "his": "m:", "equipRef": "@equip-7"}
POINT_B = {"id": "r:42", "point": "m:", "sensor": "m:", "air": "m:", "temp": "m:", "equipRef": "@equip-7"}


def _exact(markers):
    return ("brick:Air_Temperature_Sensor", 1.0) if "point" in markers else ("brick:AHU", 1.0)


def _fuzzy(markers):
    return ("brick:Air_Temperature_Sensor", 0.83)


class TestTurtleRenderer:
    def test_points_sharing_an_equip_are_distinct_nodes_of_it(self) -> None:
        out = render_turtle([SITE, AHU, POINT_A, POINT_B], _exact)
        assert "bldg:41\n    a brick:Air_Temperature_Sensor ;\n    brick:isPointOf bldg:equip-7 ." in out
        assert "bldg:42\n    a brick:Air_Temperature_Sensor ;\n    brick:isPointOf bldg:equip-7 ." in out
        assert 'bldg:equip-7\n    a brick:AHU ;\n    rdfs:label "AHU-7" ;\n    brick:hasLocation bldg:site-1 .' in out
        assert 'bldg:site-1\n    a rec:Site, brick:Site ;\n    rdfs:label "HQ" .' in out

    def test_never_emits_a_point_of_itself(self) -> None:
        out = render_turtle([{**POINT_A, "id": "@7", "equipRef": "@7"}], _exact)
        assert "isPointOf" not in out

    def test_relation_skips_a_target_brick_forbids(self) -> None:
        # equipRef naming another point: isPointOf falls through to the point's location instead.
        point = {**POINT_A, "equipRef": "r:42", "siteRef": "@site-1"}
        out = render_turtle([SITE, POINT_B, point], _exact)
        assert "bldg:41\n    a brick:Air_Temperature_Sensor ;\n    brick:isPointOf bldg:site-1 ." in out

    def test_declared_brick_class_wins_for_equipment(self) -> None:
        out = render_turtle([{**AHU, "brickClass": "brick:Air_Handler_Unit"}], _exact)
        assert "a brick:Air_Handler_Unit ;" in out

    def test_unknown_declared_class_falls_back(self) -> None:
        out = render_turtle([{**AHU, "brickClass": "brick:Not_A_Brick_Class"}], lambda m: (None, 0.0))
        assert "a brick:Equipment ;" in out

    def test_declared_system_class_is_plain_equipment(self) -> None:
        plant = {
            "id": "@equip-8",
            "equip": "m:",
            "chiller": "m:",
            "water": "m:",
            "brickClass": "brick:Chilled_Water_System",
        }
        assert "a brick:Equipment ." in render_turtle([plant], lambda m: ("brick:Chiller", 1.0))

    def test_unconfident_point_is_generic_with_a_suggestion(self) -> None:
        out = render_turtle([POINT_A], _fuzzy)
        assert "a brick:Sensor ;" in out
        assert "netix:suggestedClass brick:Air_Temperature_Sensor ;" in out
        assert 'netix:matchConfidence "0.83"^^xsd:decimal .' in out

    def test_unmapped_point_is_still_emitted(self) -> None:
        out = render_turtle([{"id": "r:9", "point": "m:", "equipRef": "@equip-7"}], lambda m: (None, 0.0))
        assert "bldg:9\n    a brick:Point ;\n    brick:isPointOf bldg:equip-7 ." in out

    def test_unsafe_ids_become_full_iris_and_labels_are_escaped(self) -> None:
        out = render_turtle([{**SITE, "id": "@p:demo/site HQ", "dis": 'Say "hi"\n'}], _exact)
        assert "<https://netix.ai/entity#p%3Ademo%2Fsite>" in out
        assert 'rdfs:label "Say \\"hi\\"\\n" .' in out

    def test_entities_without_a_kind_are_skipped(self) -> None:
        assert "bldg:5" not in render_turtle([{"id": "r:5", "dis": "loose"}], lambda m: (None, 0.0))


class TestJsonLdRenderer:
    def test_emits_typed_graph(self) -> None:
        out = render_jsonld([SITE, AHU, POINT_A], _exact)
        assert out["@context"]["brick"]
        nodes = {node["@id"]: node for node in out["@graph"]}
        assert nodes["bldg:41"]["@type"] == "brick:Air_Temperature_Sensor"
        assert nodes["bldg:41"]["brick:isPointOf"] == {"@id": "bldg:equip-7"}
        assert nodes["bldg:equip-7"]["brick:hasLocation"] == {"@id": "bldg:site-1"}
        assert nodes["bldg:site-1"]["@type"] == ["rec:Site", "brick:Site"]

    def test_unconfident_point_carries_suggestion(self) -> None:
        node = render_jsonld([POINT_A], _fuzzy)["@graph"][0]
        assert node["@type"] == "brick:Sensor"
        assert node["netix:suggestedClass"] == {"@id": "brick:Air_Temperature_Sensor"}
        assert node["netix:matchConfidence"] == {"@value": "0.83", "@type": "xsd:decimal"}

    def test_exact_match_omits_confidence(self) -> None:
        assert "netix:matchConfidence" not in render_jsonld([POINT_A], _exact)["@graph"][0]


class TestTagsToZinc:
    def test_basic(self) -> None:
        tag_dicts = [{"id": "r:1", "site": "m:", "dis": "Main"}]
        out = tags_to_zinc(tag_dicts)
        parsed = parse_zinc(out)
        assert parsed["rows"][0]["id"] == "r:1"
        assert parsed["rows"][0]["site"] == "m:"
        assert parsed["rows"][0]["dis"] == "Main"

    def test_empty_returns_header(self) -> None:
        out = tags_to_zinc([])
        assert "empty" in out

    def test_multiple_dicts(self) -> None:
        tag_dicts = [{"id": "r:1", "site": "m:"}, {"id": "r:2", "equip": "m:"}]
        out = tags_to_zinc(tag_dicts)
        parsed = parse_zinc(out)
        assert len(parsed["rows"]) == 2


class TestTagsToTrio:
    def test_basic(self) -> None:
        tag_dicts = [{"id": "r:1", "site": "m:", "dis": "Main"}]
        out = tags_to_trio(tag_dicts)
        assert "site\n" in out or "\nsite\n" in out  # bare marker key
        assert "id: @1" in out

    def test_multiple_dicts(self) -> None:
        tag_dicts = [{"id": "r:1", "site": "m:"}, {"id": "r:2", "equip": "m:"}]
        out = tags_to_trio(tag_dicts)
        assert "---" in out  # record separator present

    def test_empty_list(self) -> None:
        out = tags_to_trio([])
        assert out == "\n"


class TestTagsToJsonGrid:
    def test_basic(self) -> None:
        tag_dicts = [{"id": "r:1", "site": "m:", "area": 42}]
        result = tags_to_json_grid(tag_dicts)
        assert result["meta"]["ver"] == "3.0"
        assert any(c["name"] == "id" for c in result["cols"])
        assert result["rows"][0]["area"] == "n:42"

    def test_empty_returns_empty_grid(self) -> None:
        result = tags_to_json_grid([])
        assert result["rows"] == []
        assert result["cols"] == []

    def test_meta_override(self) -> None:
        result = tags_to_json_grid([{"id": "r:1"}], meta={"custom": "x"})
        assert result["meta"]["custom"] == "x"


class TestEncodeScalarJson:
    def test_none(self) -> None:
        assert encode_scalar_json(None) is None

    def test_bool_true(self) -> None:
        assert encode_scalar_json(True) is True

    def test_bool_false(self) -> None:
        assert encode_scalar_json(False) is False

    def test_int(self) -> None:
        assert encode_scalar_json(42) == "n:42"

    def test_float(self) -> None:
        assert encode_scalar_json(3.14) == "n:3.14"

    def test_type_prefixed_string_passthrough(self) -> None:
        assert encode_scalar_json("m:") == "m:"
        assert encode_scalar_json("r:abc") == "r:abc"

    def test_plain_string_passthrough(self) -> None:
        assert encode_scalar_json("hello") == "hello"

    def test_non_string_non_number(self) -> None:
        assert encode_scalar_json(object()) is not None  # falls back to str()


class TestZincEncodeScalar:
    def test_none(self) -> None:
        assert zinc_encode_scalar(None) == "N"

    def test_bool_true(self) -> None:
        assert zinc_encode_scalar(True) == "T"

    def test_bool_false(self) -> None:
        assert zinc_encode_scalar(False) == "F"

    def test_int(self) -> None:
        assert zinc_encode_scalar(42) == "42"

    def test_float(self) -> None:
        assert zinc_encode_scalar(3.14) == "3.14"

    def test_marker(self) -> None:
        assert zinc_encode_scalar("m:") == "M"

    def test_ref(self) -> None:
        assert zinc_encode_scalar("r:abc") == "@abc"

    def test_ref_with_display(self) -> None:
        encoded = zinc_encode_scalar("r:abc Pump 1")
        assert encoded == '@abc "Pump 1"'


class TestTrioEncodeScalar:
    def test_none(self) -> None:
        assert trio_encode_scalar(None) == "N"

    def test_bool_true(self) -> None:
        assert trio_encode_scalar(True) == "T"

    def test_bool_false(self) -> None:
        assert trio_encode_scalar(False) == "F"

    def test_int(self) -> None:
        assert trio_encode_scalar(42) == "42"

    def test_marker(self) -> None:
        assert trio_encode_scalar("m:") == ""

    def test_ref(self) -> None:
        assert trio_encode_scalar("r:abc") == "@abc"
