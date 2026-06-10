"""Parser tests — Zinc, Trio, Haystack 4 JSON."""

from __future__ import annotations

import pytest

from haystack_sdk import iter_entities, parse_grid, parse_json, parse_trio, parse_zinc


class TestZincParser:
    def test_minimal_grid(self) -> None:
        text = 'ver:"3.0"\nid,dis\n@1,"A"\n'
        grid = parse_zinc(text)
        assert grid["meta"] == {"ver": "3.0"}
        assert [c["name"] for c in grid["cols"]] == ["id", "dis"]
        assert grid["rows"] == [{"id": "r:1", "dis": "A"}]

    def test_markers_bools_null(self) -> None:
        text = 'ver:"3.0"\nid,site,active,note\n@1,M,T,N\n@2,M,F,"hi"\n'
        grid = parse_zinc(text)
        assert grid["rows"][0] == {"id": "r:1", "site": "m:", "active": True, "note": None}
        assert grid["rows"][1] == {"id": "r:2", "site": "m:", "active": False, "note": "hi"}

    def test_numeric_with_unit(self) -> None:
        text = 'ver:"3.0"\nid,area\n@1,1500\n@2,3.14\n'
        grid = parse_zinc(text)
        assert grid["rows"][0]["area"] == 1500
        assert grid["rows"][1]["area"] == 3.14

    def test_empty_body_raises(self) -> None:
        with pytest.raises(ValueError):
            parse_zinc("")

    def test_skips_blank_lines(self) -> None:
        text = 'ver:"3.0"\nid\n@1\n\n@2\n'
        grid = parse_zinc(text)
        assert len(grid["rows"]) == 2


class TestTrioParser:
    def test_simple_block(self) -> None:
        text = "id: @1\ndis: Pump-1\npoint\nsensor\n"
        grid = parse_trio(text)
        assert grid["rows"] == [{"id": "r:1", "dis": "Pump-1", "point": "m:", "sensor": "m:"}]

    def test_multiple_blocks(self) -> None:
        text = "id: @1\nsite\n---\nid: @2\nequip\n"
        grid = parse_trio(text)
        assert len(grid["rows"]) == 2
        assert grid["rows"][0] == {"id": "r:1", "site": "m:"}
        assert grid["rows"][1] == {"id": "r:2", "equip": "m:"}

    def test_skips_comments(self) -> None:
        text = "// this is a comment\nid: @1\nsite\n"
        grid = parse_trio(text)
        assert grid["rows"] == [{"id": "r:1", "site": "m:"}]


class TestJsonParser:
    def test_round_trip(self) -> None:
        text = '{"meta":{"ver":"3.0"},"cols":[{"name":"id"}],"rows":[{"id":"r:1"}]}'
        grid = parse_json(text)
        assert grid["meta"]["ver"] == "3.0"
        assert grid["rows"] == [{"id": "r:1"}]

    def test_invalid_json_raises(self) -> None:
        with pytest.raises(ValueError):
            parse_json("not json")

    def test_non_object_raises(self) -> None:
        with pytest.raises(ValueError):
            parse_json("[]")


class TestParseGridDispatch:
    def test_unknown_format_raises(self) -> None:
        with pytest.raises(ValueError):
            parse_grid("...", format="yaml")

    def test_dispatches_zinc(self) -> None:
        grid = parse_grid('ver:"3.0"\nid\n@1\n', format="zinc")
        assert grid["rows"] == [{"id": "r:1"}]


class TestIterEntities:
    def test_zinc_yields_rows(self) -> None:
        text = 'ver:"3.0"\nid,dis\n@1,"A"\n@2,"B"\n'
        entities = list(iter_entities(text, format="zinc"))
        assert len(entities) == 2
        assert entities[0] == {"id": "r:1", "dis": "A"}
        assert entities[1] == {"id": "r:2", "dis": "B"}

    def test_trio_yields_rows(self) -> None:
        text = "id: @1\nsite\n---\nid: @2\nequip\n"
        entities = list(iter_entities(text, format="trio"))
        assert len(entities) == 2

    def test_json_yields_rows(self) -> None:
        text = '{"meta":{"ver":"3.0"},"cols":[{"name":"id"}],"rows":[{"id":"r:1"},{"id":"r:2"}]}'
        entities = list(iter_entities(text, format="json"))
        assert len(entities) == 2
        assert entities[0]["id"] == "r:1"

    def test_unknown_format_raises(self) -> None:
        with pytest.raises(ValueError):
            list(iter_entities("...", format="csv"))


class TestZincSplitCellsEdgeCases:
    """Edge cases in _split_cells — embedded commas inside quoted strings."""

    def test_embedded_comma_in_quoted_string(self) -> None:
        text = 'ver:"3.0"\nid,dis\n@1,"Hello, world"\n'
        grid = parse_zinc(text)
        assert grid["rows"][0]["dis"] == "Hello, world"

    def test_multiple_quoted_cells_with_commas(self) -> None:
        text = 'ver:"3.0"\na,b,c\n"one, two","three","four, five"\n'
        grid = parse_zinc(text)
        assert grid["rows"][0] == {"a": "one, two", "b": "three", "c": "four, five"}
