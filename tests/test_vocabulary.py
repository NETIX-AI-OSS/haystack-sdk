"""Vocabulary tests — pack contents + helpers."""

from __future__ import annotations

from haystack_sdk import (
    ALL_PACKS,
    CORE,
    DISTRICT_COOLING,
    FDD,
    HEALTHCARE,
    NETIX_CUSTOM,
    RESIDENTIAL,
    RETAIL_MALL,
    WATER_TREATMENT,
    Vocabulary,
    get_tag_def,
    validate_markers,
)


def test_all_packs_present() -> None:
    expected = {CORE, FDD, NETIX_CUSTOM, RETAIL_MALL, RESIDENTIAL, HEALTHCARE, WATER_TREATMENT, DISTRICT_COOLING}
    assert set(ALL_PACKS) == expected


def test_core_has_expected_markers() -> None:
    names = CORE.names()
    for required in ("site", "building", "floor", "space", "equip", "device", "point", "ahu", "vav", "his"):
        assert required in names, f"missing core tag: {required}"


def test_get_tag_def_finds_core() -> None:
    tag = get_tag_def("ahu")
    assert tag is not None
    assert tag.is_marker
    assert tag.namespace == "phIoT"


def test_get_tag_def_unknown_returns_none() -> None:
    assert get_tag_def("nonexistent_tag_xyz") is None


def test_validate_markers_partitions() -> None:
    result = validate_markers({"site", "ahu", "definitely_unknown"})
    assert "site" in result.known
    assert "ahu" in result.known
    assert "definitely_unknown" in result.unknown
    assert not result.is_valid


def test_validate_markers_with_extra() -> None:
    result = validate_markers({"my_custom"}, extra={"my_custom"})
    assert result.is_valid
    assert "my_custom" in result.known


def test_vocabulary_is_frozen() -> None:
    # Vocabulary uses frozen dataclasses — should not allow mutation
    import pytest

    with pytest.raises((AttributeError, TypeError)):
        CORE.tags = ()  # type: ignore[misc]


def test_tagdef_is_hashable() -> None:
    tag = get_tag_def("site")
    assert tag is not None
    # Frozen dataclass → hashable
    {tag}


def test_pack_membership() -> None:
    assert "site" in CORE
    assert "site" not in WATER_TREATMENT


def test_all_packs_have_version() -> None:
    for pack in ALL_PACKS:
        assert isinstance(pack, Vocabulary)
        assert pack.version
        assert pack.name
        assert len(pack) > 0
