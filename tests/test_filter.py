"""Filter parser + evaluator tests."""

from __future__ import annotations

import pytest

from haystack_sdk import (
    AndNode,
    CmpNode,
    MarkerNode,
    NotNode,
    OrNode,
    evaluate_filter,
    parse_filter,
)


class TestParser:
    def test_empty_returns_no_node(self) -> None:
        ast = parse_filter("")
        assert ast.is_empty

    def test_single_marker(self) -> None:
        ast = parse_filter("site")
        assert isinstance(ast.node, MarkerNode)
        assert ast.node.name == "site"

    def test_and(self) -> None:
        ast = parse_filter("point and his")
        assert isinstance(ast.node, AndNode)
        assert len(ast.node.children) == 2

    def test_or(self) -> None:
        ast = parse_filter("site or equip")
        assert isinstance(ast.node, OrNode)

    def test_not(self) -> None:
        ast = parse_filter("not point")
        assert isinstance(ast.node, NotNode)

    def test_parenthesized(self) -> None:
        ast = parse_filter("(site and area > 1000) or equip")
        assert isinstance(ast.node, OrNode)
        assert isinstance(ast.node.children[0], AndNode)

    def test_ref_comparison(self) -> None:
        ast = parse_filter("equipRef==@42")
        assert isinstance(ast.node, CmpNode)
        assert ast.node.path == ["equipRef"]
        assert ast.node.value == "@42"
        assert ast.refs == {"equipRef": "@42"}

    def test_numeric(self) -> None:
        ast = parse_filter("area > 1000")
        assert isinstance(ast.node, CmpNode)
        assert ast.node.value == 1000


class TestEvaluator:
    def test_marker_present(self) -> None:
        assert evaluate_filter({"site": "m:"}, MarkerNode("site")) is True
        assert evaluate_filter({"point": "m:"}, MarkerNode("site")) is False

    def test_and_short_circuits(self) -> None:
        node = parse_filter("point and his").node
        assert evaluate_filter({"point": "m:", "his": "m:"}, node) is True  # type: ignore[arg-type]
        assert evaluate_filter({"point": "m:"}, node) is False  # type: ignore[arg-type]

    def test_or(self) -> None:
        node = parse_filter("site or equip").node
        assert evaluate_filter({"site": "m:"}, node) is True  # type: ignore[arg-type]
        assert evaluate_filter({"point": "m:"}, node) is False  # type: ignore[arg-type]

    def test_not(self) -> None:
        node = parse_filter("not point").node
        assert evaluate_filter({"site": "m:"}, node) is True  # type: ignore[arg-type]
        assert evaluate_filter({"point": "m:"}, node) is False  # type: ignore[arg-type]

    def test_numeric_comparison_strips_prefix(self) -> None:
        node = parse_filter("area > 1000").node
        # Entity value stored as a typed-JSON string ("n:1500")
        assert evaluate_filter({"area": "n:1500"}, node) is True  # type: ignore[arg-type]
        assert evaluate_filter({"area": "n:500"}, node) is False  # type: ignore[arg-type]

    def test_ref_path_with_resolver(self) -> None:
        # equip points to site
        graph = {
            "@equip1": {"id": "r:equip1", "equip": "m:", "siteRef": "@site1"},
            "@site1": {"id": "r:site1", "site": "m:", "dis": "Main"},
        }

        def resolver(ref: str):
            return graph.get(ref)

        node = parse_filter("equipRef->siteRef==@site1").node
        point = {"id": "r:p1", "point": "m:", "equipRef": "@equip1"}
        # Single-step works
        assert evaluate_filter(point, node, resolver=resolver) is True  # type: ignore[arg-type]

    def test_ref_path_without_resolver_returns_false(self) -> None:
        node = parse_filter("equipRef->siteRef==@x").node
        assert evaluate_filter({"equipRef": "@1"}, node) is False  # type: ignore[arg-type]


class TestAstHelpers:
    def test_evaluate_method(self) -> None:
        ast = parse_filter("site")
        assert ast.evaluate({"site": "m:"}) is True

    def test_empty_evaluate_true(self) -> None:
        ast = parse_filter("")
        assert ast.evaluate({}) is True


def test_invalid_filter_raises() -> None:
    with pytest.raises(ValueError):
        parse_filter("(unbalanced")
