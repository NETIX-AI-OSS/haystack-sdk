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
)

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
