"""AUTO-GENERATED from haystack_sdk/vocabulary/data/netix_custom_tags.json — DO NOT EDIT BY HAND.

Regenerate with::

    python scripts/generate_vocabulary.py
"""

from __future__ import annotations

from haystack_sdk.vocabulary._base import TagDef, Vocabulary

CLINIC_SPACE = TagDef(
    name="clinicSpace", display_name="Clinic Space", kind=0, namespace="netix", doc="Space is a diagnostic clinic room"
)
OR_ROOM = TagDef(name="orRoom", display_name="OR Room", kind=0, namespace="netix", doc="Operating/procedure room")
MRI_ROOM = TagDef(
    name="mriRoom", display_name="MRI Room", kind=0, namespace="netix", doc="MRI suite with RF isolation requirement"
)
RF_ISOLATOR = TagDef(
    name="rfIsolator", display_name="RF Isolator", kind=0, namespace="netix", doc="Equipment is an RF isolator circuit"
)
SUB_METER = TagDef(
    name="subMeter",
    display_name="Sub Meter",
    kind=0,
    namespace="netix",
    doc="Equipment is an electrical sub-meter (extends meter)",
)
PROTOCOL = TagDef(
    name="protocol",
    display_name="Protocol",
    kind=3,
    namespace="netix",
    doc="Wire protocol: modbus-rtu, bacnet-ip, snmp-v3, mqtt",
)
MODBUS_REGISTER = TagDef(
    name="modbusRegister",
    display_name="Modbus Register",
    kind=2,
    namespace="netix",
    doc="Source Modbus register address",
)
BACNET_OBJECT_ID = TagDef(
    name="bacnetObjectId",
    display_name="BACnet Object ID",
    kind=3,
    namespace="netix",
    doc="Source BACnet object identifier",
)
MANUAL_TAG = TagDef(
    name="manualTag",
    display_name="Manual Tag",
    kind=0,
    namespace="netix",
    doc="Point was manually tagged (not auto-tagged)",
)

NETIX_CUSTOM = Vocabulary(
    name="netix_custom",
    version="1.0.0",
    tags=(
        CLINIC_SPACE,
        OR_ROOM,
        MRI_ROOM,
        RF_ISOLATOR,
        SUB_METER,
        PROTOCOL,
        MODBUS_REGISTER,
        BACNET_OBJECT_ID,
        MANUAL_TAG,
    ),
)
