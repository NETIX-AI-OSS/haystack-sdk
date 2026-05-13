"""AUTO-GENERATED from haystack_sdk/vocabulary/data/district_cooling_tags.json — DO NOT EDIT BY HAND.

Regenerate with::

    python scripts/generate_vocabulary.py
"""

from __future__ import annotations

from haystack_sdk.vocabulary._base import TagDef, Vocabulary

DC_PLANT = TagDef(
    name="dcPlant",
    display_name="District Cooling Plant",
    kind=0,
    namespace="netix",
    doc="Site is a district cooling production and distribution plant",
)
ENERGY_TRANSFER_STATION = TagDef(
    name="energyTransferStation",
    display_name="Energy Transfer Station",
    kind=0,
    namespace="netix",
    doc="Customer energy transfer station (ETS) — hydraulic separation between primary distribution and secondary building loop",
)
CHW_FLOW_METER = TagDef(
    name="chwFlowMeter",
    display_name="CHW Flow Meter",
    kind=0,
    namespace="netix",
    doc="Chilled water BTU/flow meter for customer or zone energy metering",
)
PRIMARY_LOOP = TagDef(
    name="primaryLoop",
    display_name="Primary Loop",
    kind=0,
    namespace="netix",
    doc="Point or equipment is on the primary chilled water production loop",
)
SECONDARY_LOOP = TagDef(
    name="secondaryLoop",
    display_name="Secondary Loop",
    kind=0,
    namespace="netix",
    doc="Point or equipment is on the secondary chilled water distribution loop",
)
THERMAL_STORAGE = TagDef(
    name="thermalStorage",
    display_name="Thermal Storage",
    kind=0,
    namespace="netix",
    doc="Thermal energy storage tank (chilled water accumulator or ice storage)",
)
PRESSURE_BREAK_STATION = TagDef(
    name="pressureBreakStation",
    display_name="Pressure Break Station",
    kind=0,
    namespace="netix",
    doc="Pressure-breaking or pressure-sustaining station between loop pressure zones",
)

PACK = Vocabulary(
    name="district_cooling",
    version="1.0.0",
    tags=(
        DC_PLANT,
        ENERGY_TRANSFER_STATION,
        CHW_FLOW_METER,
        PRIMARY_LOOP,
        SECONDARY_LOOP,
        THERMAL_STORAGE,
        PRESSURE_BREAK_STATION,
    ),
)
