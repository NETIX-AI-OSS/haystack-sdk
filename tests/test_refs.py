"""Ref parsing tests."""

from __future__ import annotations

import pytest

from haystack_sdk import Ref, is_ref, normalize_ref, parse_ref


def test_parse_at_form() -> None:
    ref = parse_ref("@abc")
    assert ref == Ref(id="abc")


def test_parse_with_dis() -> None:
    ref = parse_ref("@abc Pump-1")
    assert ref == Ref(id="abc", dis="Pump-1")


def test_parse_quoted_dis() -> None:
    ref = parse_ref('@abc "Pump 1"')
    assert ref == Ref(id="abc", dis="Pump 1")


def test_parse_typed_json() -> None:
    ref = parse_ref("r:abc")
    assert ref == Ref(id="abc")


def test_invalid_raises() -> None:
    with pytest.raises(ValueError):
        parse_ref("not-a-ref")


def test_invalid_id_chars_raise() -> None:
    with pytest.raises(ValueError):
        Ref(id="bad chars!")


def test_is_ref() -> None:
    assert is_ref("@abc")
    assert is_ref("r:abc")
    assert not is_ref("plain")
    assert not is_ref(42)
    assert not is_ref(None)


def test_normalize_ref() -> None:
    assert normalize_ref("@abc") == "r:abc"
    assert normalize_ref("r:abc") == "r:abc"
    assert normalize_ref("@abc Pump") == "r:abc Pump"


def test_zinc_encoding() -> None:
    assert Ref("abc").to_zinc() == "@abc"
    assert Ref("abc", "Pump").to_zinc() == '@abc "Pump"'


def test_trio_encoding_strips_dis() -> None:
    # Trio refs are bare; dis comes from a separate `dis` line.
    assert Ref("abc", "Pump").to_trio() == "@abc"
