"""AUTO-GENERATED from haystack_sdk/vocabulary/data/smart_residential_tags.json — DO NOT EDIT BY HAND.

Regenerate with::

    python scripts/generate_vocabulary.py
"""

from __future__ import annotations

from haystack_sdk.vocabulary._base import TagDef, Vocabulary

FAHU = TagDef(
    name="fahu",
    display_name="Fresh Air Handling Unit",
    kind=0,
    namespace="netix",
    doc="Equipment is a fresh/outdoor air handling unit (FAHU); subtype of ahu",
)
OAHU = TagDef(
    name="oahu",
    display_name="Outdoor Air Handling Unit",
    kind=0,
    namespace="netix",
    doc="Equipment is an outdoor air handling unit (OAHU); subtype of ahu",
)
IAQ_SENSOR = TagDef(
    name="iaqSensor",
    display_name="IAQ Sensor",
    kind=0,
    namespace="netix",
    doc="Equipment is an indoor air quality (IAQ) multi-sensor device",
)
CHW_PUMP = TagDef(
    name="chwPump",
    display_name="Chilled Water Pump",
    kind=0,
    namespace="netix",
    doc="Equipment is a chilled water circulating pump",
)
LIFT = TagDef(
    name="lift",
    display_name="Lift / Elevator",
    kind=0,
    namespace="netix",
    doc="Equipment is a passenger or service lift",
)
PM2P5 = TagDef(
    name="pm2p5",
    display_name="PM 2.5",
    kind=0,
    namespace="netix",
    doc="Point measures PM 2.5 fine particulate concentration",
)
PM10 = TagDef(
    name="pm10",
    display_name="PM 10",
    kind=0,
    namespace="netix",
    doc="Point measures PM 10 coarse particulate concentration",
)
TVOC = TagDef(
    name="tvoc",
    display_name="TVOC",
    kind=0,
    namespace="netix",
    doc="Point measures total volatile organic compound (TVOC) concentration",
)
CH2O = TagDef(
    name="ch2o",
    display_name="CH2O / Formaldehyde",
    kind=0,
    namespace="netix",
    doc="Point measures formaldehyde (CH2O) concentration",
)
FIRE_ALARM = TagDef(
    name="fireAlarm",
    display_name="Fire Alarm",
    kind=0,
    namespace="netix",
    doc="Point is a fire alarm status or trigger signal",
)
HOA = TagDef(
    name="hoa",
    display_name="HOA Mode",
    kind=0,
    namespace="netix",
    doc="Point indicates hand/off/auto (HOA) control mode",
)
FILTER_STATUS = TagDef(
    name="filterStatus",
    display_name="Filter Status",
    kind=0,
    namespace="netix",
    doc="Point indicates air filter condition or differential pressure status",
)

RESIDENTIAL = Vocabulary(
    name="residential",
    version="1.0.0",
    tags=(
        FAHU,
        OAHU,
        IAQ_SENSOR,
        CHW_PUMP,
        LIFT,
        PM2P5,
        PM10,
        TVOC,
        CH2O,
        FIRE_ALARM,
        HOA,
        FILTER_STATUS,
    ),
)
