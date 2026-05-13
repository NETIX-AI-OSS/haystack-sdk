"""Golden-grid round-trip tests.

Parse → render → re-parse must yield equal row dicts. Locks the wire-format
contract so future renderer/parser tweaks don't silently change output.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from haystack_sdk import parse_zinc, render_zinc

FIXTURES = Path(__file__).parent / "fixtures" / "golden_grids"


@pytest.mark.parametrize("fixture_name", [p.name for p in FIXTURES.glob("*.zinc")])
def test_zinc_round_trip(fixture_name: str) -> None:
    original = (FIXTURES / fixture_name).read_text()
    grid = parse_zinc(original)
    re_rendered = render_zinc(grid)
    re_parsed = parse_zinc(re_rendered)
    assert re_parsed["rows"] == grid["rows"]
    assert [c["name"] for c in re_parsed["cols"]] == [c["name"] for c in grid["cols"]]
