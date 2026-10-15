"""Brick class registry tests."""

from __future__ import annotations

import pytest

from haystack_sdk import (
    BRICK_VERSION,
    BrickClass,
    brick_class_kind,
    find_brick_class,
    normalize_brick_class,
    validate_brick_class,
)
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
    # Any class of the bundled ontology, not only the registry's.
    assert validate_brick_class("brick:Chilled_Water_Valve")
    assert not validate_brick_class("brick:Made_Up_Thing")


def test_iter_brick_classes() -> None:
    classes = list(iter_brick_classes())
    assert len(classes) > 0
    assert all(isinstance(c, BrickClass) for c in classes)


def test_jaccard() -> None:
    assert jaccard_similarity(["a", "b"], ["a", "b"]) == 1.0
    assert jaccard_similarity(["a", "b"], ["a", "c"]) == pytest.approx(1 / 3)
    assert jaccard_similarity([], []) == 0.0


def test_historized_point_still_maps_exactly() -> None:
    # his/cur/writable say how a point is read, not what it is; they used to defeat every exact match.
    qname, conf = find_brick_class(["air", "cur", "his", "point", "sensor", "temp", "writable"])
    assert (qname, conf) == ("brick:Air_Temperature_Sensor", 1.0)


def test_most_specific_covering_mapping_wins() -> None:
    qname, conf = find_brick_class(["air", "discharge", "his", "point", "sensor", "temp"])
    assert (qname, conf) == ("brick:Discharge_Air_Temperature_Sensor", 1.0)


def test_inherited_equipment_markers_do_not_turn_a_point_into_equipment() -> None:
    # tag-service layers the parent asset class's markers (equip, ahu, air) into each point dict.
    qname, conf = find_brick_class(["ahu", "air", "equip", "fan", "point", "run", "sensor"])
    assert (qname, conf) == ("brick:Fan_On_Off_Status", 1.0)


def test_equipment_markers_resolve_to_equipment() -> None:
    qname, conf = find_brick_class(["ahu", "air", "equip"])
    assert (qname, conf) == ("brick:AHU", 1.0)


def test_ambiguous_covering_mappings_fall_back_to_fuzzy() -> None:
    qname, conf = find_brick_class(["air", "point", "sensor", "sp", "temp", "zone"])
    assert qname in {"brick:Zone_Air_Temperature_Sensor", "brick:Zone_Air_Temperature_Setpoint"}
    assert conf < 1.0


def test_no_covering_mapping_is_fuzzy() -> None:
    qname, conf = find_brick_class(["his", "point", "sensor", "temp", "water"])
    assert qname is not None
    assert conf < 1.0


def test_registry_classes_exist_in_bundled_brick() -> None:
    for entry in iter_brick_classes():
        kind = brick_class_kind(entry.brick_class)
        assert kind is not None, entry.brick_class
        assert (kind == "point") == ("point" in entry.haystack_tags), entry


def test_normalize_brick_class() -> None:
    assert normalize_brick_class("brick:AHU") == "brick:AHU"
    assert normalize_brick_class("Chiller") == "brick:Chiller"
    assert normalize_brick_class("https://brickschema.org/schema/Brick#Pump") == "brick:Pump"
    assert normalize_brick_class("brick:UPS") is None
    assert normalize_brick_class("") is None
    assert normalize_brick_class(None) is None


def test_brick_class_kind() -> None:
    assert brick_class_kind("brick:Air_Handler_Unit") == "equipment"
    assert brick_class_kind("brick:Supply_Air_Temperature_Sensor") == "point"
    assert brick_class_kind("brick:Site") == "location"
    assert brick_class_kind("brick:Chilled_Water_System") == "system"
    assert brick_class_kind("brick:Made_Up_Thing") is None
    assert BRICK_VERSION.startswith("1.4")
