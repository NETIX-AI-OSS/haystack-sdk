"""Brick class registry tests."""

from __future__ import annotations

import pytest

from haystack_sdk import BrickClass, find_brick_class, validate_brick_class
from haystack_sdk.brick import iter_brick_classes, jaccard_similarity


def test_exact_match() -> None:
    qname, conf = find_brick_class(["air", "point", "sensor", "temp"])
    assert qname == "brick:Air_Temperature_Sensor"
    assert conf == 1.0


def test_unknown_combo_returns_none() -> None:
    qname, conf = find_brick_class(["totally", "unknown", "tags"])
    assert qname is None
    assert conf == 0.0


def test_fuzzy_match_below_threshold() -> None:
    qname, _ = find_brick_class(["temp"])
    assert qname is None


def test_extra_classes_injected() -> None:
    extra = (
        BrickClass(
            name="custom-thing",
            display_name="Custom",
            haystack_tags=("custom", "marker"),
            brick_class="brick:Custom_Thing",
        ),
    )
    qname, conf = find_brick_class(["custom", "marker"], extra=extra)
    assert qname == "brick:Custom_Thing"
    assert conf == 1.0


def test_validate_brick_class() -> None:
    assert validate_brick_class("brick:Air_Temperature_Sensor")
    assert not validate_brick_class("brick:Made_Up_Thing")


def test_iter_brick_classes() -> None:
    classes = list(iter_brick_classes())
    assert len(classes) > 0
    assert all(isinstance(c, BrickClass) for c in classes)


def test_jaccard() -> None:
    assert jaccard_similarity(["a", "b"], ["a", "b"]) == 1.0
    assert jaccard_similarity(["a", "b"], ["a", "c"]) == pytest.approx(1 / 3)
    assert jaccard_similarity([], []) == 0.0
