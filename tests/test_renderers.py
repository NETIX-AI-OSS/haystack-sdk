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


class TestTurtleRenderer:
    def _resolver(self, markers):
        if sorted(markers) == ["air", "point", "sensor", "temp"]:
            return ("brick:Air_Temperature_Sensor", 1.0)
        return (None, 0.0)

    def test_emits_type_triple(self) -> None:
        tags = [{"id": "r:42", "point": "m:", "sensor": "m:", "air": "m:", "temp": "m:"}]
        out = render_turtle(tags, self._resolver)
        assert "netix:42" in out
        assert "brick:Air_Temperature_Sensor" in out

    def test_fuzzy_match_comment_keeps_valid_separator(self) -> None:
        # Regression: a fuzzy-match note must trail the ';'/'.' separator. A
        # Turtle '#' comment runs to end-of-line, so a note placed before the
        # separator swallows it and yields invalid RDF.
        tags = [{"id": "r:42", "point": "m:", "sensor": "m:", "air": "m:", "temp": "m:", "equipRef": "r:7"}]
        out = render_turtle(tags, lambda markers: ("brick:Air_Temperature_Sensor", 0.83))
        assert "# fuzzy match (0.83)" in out
        # On any line carrying the fuzzy-match note, the ';'/'.' separator must
        # come *before* the comment (a '#' comment runs to end-of-line).
        for line in out.splitlines():
            idx = line.find("# fuzzy match")
            if idx != -1:
                before = line[:idx].rstrip()
                assert before.endswith((";", ".")), f"separator swallowed by comment: {line!r}"
        # The type line keeps its separator before the note.
        assert any(";  # fuzzy match (0.83)" in line for line in out.splitlines())


class TestJsonLdRenderer:
    def _resolver(self, markers):
        return ("brick:Air_Temperature_Sensor", 1.0)

    def test_emits_graph(self) -> None:
        tags = [{"id": "r:42", "point": "m:", "sensor": "m:", "air": "m:", "temp": "m:", "equipRef": "r:7"}]
        out = render_jsonld(tags, self._resolver)
        assert out["@context"]["brick"]
        assert out["@graph"][0]["@type"] == "brick:Air_Temperature_Sensor"
        assert out["@graph"][0]["brick:isPointOf"] == {"@id": "netix:7"}

    def test_fuzzy_match_emits_confidence(self) -> None:
        """When confidence < 1.0, render_jsonld should emit netix:matchConfidence."""

        def fuzzy_resolver(markers):
            return ("brick:Temperature_Sensor", 0.75)

        tags = [{"id": "r:9", "point": "m:", "temp": "m:"}]
        out = render_jsonld(tags, fuzzy_resolver)
        node = out["@graph"][0]
        assert node["@type"] == "brick:Temperature_Sensor"
        assert "netix:matchConfidence" in node
        assert abs(node["netix:matchConfidence"] - 0.75) < 1e-9

    def test_exact_match_omits_confidence(self) -> None:
        """Exact matches (confidence == 1.0) must NOT emit netix:matchConfidence."""

        def exact_resolver(markers):
            return ("brick:Temperature_Sensor", 1.0)

        tags = [{"id": "r:9", "point": "m:", "temp": "m:"}]
        out = render_jsonld(tags, exact_resolver)
        assert "netix:matchConfidence" not in out["@graph"][0]


class TestTurtleFuzzyMatch:
    def test_fuzzy_match_adds_comment(self) -> None:
        """confidence < 1.0 should embed a '# fuzzy match' comment in the triple."""

        def fuzzy_resolver(markers):
            return ("brick:Temperature_Sensor", 0.8)

        tags = [{"id": "r:10", "point": "m:", "temp": "m:"}]
        out = render_turtle(tags, fuzzy_resolver)
        assert "fuzzy match" in out
        assert "0.80" in out

    def test_exact_match_no_comment(self) -> None:
        """confidence == 1.0 should NOT add a fuzzy-match comment."""

        def exact_resolver(markers):
            return ("brick:Temperature_Sensor", 1.0)

        tags = [{"id": "r:10", "point": "m:", "temp": "m:"}]
        out = render_turtle(tags, exact_resolver)
        assert "fuzzy match" not in out


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
