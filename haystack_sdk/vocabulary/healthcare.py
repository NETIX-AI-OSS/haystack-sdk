"""AUTO-GENERATED from haystack_sdk/vocabulary/data/healthcare_tags.json — DO NOT EDIT BY HAND.

Regenerate with::

    python scripts/generate_vocabulary.py
"""

from __future__ import annotations

from haystack_sdk.vocabulary._base import TagDef, Vocabulary

HOSPITAL = TagDef(
    name="hospital", display_name="Hospital", kind=0, namespace="netix", doc="Site is a hospital or healthcare facility"
)
ICU_ROOM = TagDef(
    name="icuRoom",
    display_name="ICU Room",
    kind=0,
    namespace="netix",
    doc="Space is an Intensive Care Unit room — critical HVAC and monitoring requirements",
)
ISOLATION_ROOM = TagDef(
    name="isolationRoom",
    display_name="Isolation Room",
    kind=0,
    namespace="netix",
    doc="Space is a clinical isolation room (positive or negative pressure controlled)",
)
NEG_PRESSURE_ROOM = TagDef(
    name="negPressureRoom",
    display_name="Negative Pressure Room",
    kind=0,
    namespace="netix",
    doc="Negative pressure isolation room for airborne infection control (e.g. TB, COVID)",
)
POS_PRESSURE_ROOM = TagDef(
    name="posPressureRoom",
    display_name="Positive Pressure Room",
    kind=0,
    namespace="netix",
    doc="Positive pressure protective environment room for immunocompromised patients",
)
STERILE_ZONE = TagDef(
    name="sterileZone",
    display_name="Sterile Zone",
    kind=0,
    namespace="netix",
    doc="Sterile processing zone or clean room — HVAC pressure, filtration, and humidity are critical",
)
PHARMACY_COLD_ROOM = TagDef(
    name="pharmacyColdRoom",
    display_name="Pharmacy Cold Room",
    kind=0,
    namespace="netix",
    doc="Pharmacy refrigerated storage space — temperature and humidity alarming required",
)
LAB_ROOM = TagDef(
    name="labRoom",
    display_name="Lab Room",
    kind=0,
    namespace="netix",
    doc="Medical or research laboratory space — fume extraction and pressure differential requirements",
)

PACK = Vocabulary(
    name="healthcare",
    version="1.0.0",
    tags=(
        HOSPITAL,
        ICU_ROOM,
        ISOLATION_ROOM,
        NEG_PRESSURE_ROOM,
        POS_PRESSURE_ROOM,
        STERILE_ZONE,
        PHARMACY_COLD_ROOM,
        LAB_ROOM,
    ),
)
