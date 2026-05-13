"""AUTO-GENERATED from haystack_sdk/vocabulary/data/core_tags.json — DO NOT EDIT BY HAND.

Regenerate with::

    python scripts/generate_vocabulary.py
"""

from __future__ import annotations

from haystack_sdk.vocabulary._base import TagDef, Vocabulary

SITE = TagDef(
    name="site",
    display_name="Site",
    kind=0,
    namespace="phIoT",
    doc="Site is a geographic location of a building or campus",
)
BUILDING = TagDef(name="building", display_name="Building", kind=0, namespace="phIoT", doc="Building within a site")
FLOOR = TagDef(name="floor", display_name="Floor", kind=0, namespace="phIoT", doc="Floor of a building")
SPACE = TagDef(
    name="space", display_name="Space", kind=0, namespace="phIoT", doc="Enclosed room or area within a floor"
)
EQUIP = TagDef(
    name="equip", display_name="Equipment", kind=0, namespace="phIoT", doc="Physical or logical piece of equipment"
)
DEVICE = TagDef(
    name="device", display_name="Device", kind=0, namespace="phIoT", doc="Microprocessor based hardware device"
)
POINT = TagDef(
    name="point", display_name="Point", kind=0, namespace="phIoT", doc="Data point such as a sensor or actuator"
)
SENSOR = TagDef(name="sensor", display_name="Sensor", kind=0, namespace="phIoT", doc="Point is a sensor input")
CMD = TagDef(name="cmd", display_name="Command", kind=0, namespace="phIoT", doc="Point is a command output")
SP = TagDef(name="sp", display_name="Setpoint", kind=0, namespace="phIoT", doc="Point is a setpoint")
HIS = TagDef(name="his", display_name="History", kind=0, namespace="phIoT", doc="Point has historical time-series data")
WRITABLE = TagDef(
    name="writable", display_name="Writable", kind=0, namespace="phIoT", doc="Point supports writing/commanding"
)
CUR = TagDef(
    name="cur", display_name="Current Value", kind=0, namespace="phIoT", doc="Point supports real-time current value"
)
AIR = TagDef(name="air", display_name="Air", kind=0, namespace="phIoT", doc="Related to air")
WATER = TagDef(name="water", display_name="Water", kind=0, namespace="phIoT", doc="Related to water")
STEAM = TagDef(name="steam", display_name="Steam", kind=0, namespace="phIoT", doc="Related to steam")
ELEC = TagDef(name="elec", display_name="Electric", kind=0, namespace="phIoT", doc="Related to electricity")
GAS = TagDef(name="gas", display_name="Gas", kind=0, namespace="phIoT", doc="Related to natural gas")
TEMP = TagDef(
    name="temp",
    display_name="Temperature",
    kind=0,
    namespace="phIoT",
    doc="Temperature measurement",
    unit_quantity="temperature",
)
HUMIDITY = TagDef(
    name="humidity",
    display_name="Humidity",
    kind=0,
    namespace="phIoT",
    doc="Humidity measurement",
    unit_quantity="humidity",
)
PRESSURE = TagDef(
    name="pressure",
    display_name="Pressure",
    kind=0,
    namespace="phIoT",
    doc="Pressure measurement",
    unit_quantity="pressure",
)
FLOW = TagDef(
    name="flow", display_name="Flow", kind=0, namespace="phIoT", doc="Flow rate measurement", unit_quantity="flow"
)
CO2 = TagDef(name="co2", display_name="CO2", kind=0, namespace="phIoT", doc="Carbon dioxide concentration")
POWER = TagDef(
    name="power",
    display_name="Power",
    kind=0,
    namespace="phIoT",
    doc="Electrical power measurement",
    unit_quantity="power",
)
ENERGY = TagDef(
    name="energy",
    display_name="Energy",
    kind=0,
    namespace="phIoT",
    doc="Energy consumption measurement",
    unit_quantity="energy",
)
VOLT = TagDef(
    name="volt", display_name="Voltage", kind=0, namespace="phIoT", doc="Electrical voltage", unit_quantity="voltage"
)
CURRENT = TagDef(
    name="current", display_name="Current", kind=0, namespace="phIoT", doc="Electrical current", unit_quantity="current"
)
FREQ = TagDef(
    name="freq",
    display_name="Frequency",
    kind=0,
    namespace="phIoT",
    doc="Frequency measurement",
    unit_quantity="frequency",
)
PF = TagDef(name="pf", display_name="Power Factor", kind=0, namespace="phIoT", doc="Power factor")
SPEED = TagDef(name="speed", display_name="Speed", kind=0, namespace="phIoT", doc="Speed or velocity measurement")
LEVEL = TagDef(name="level", display_name="Level", kind=0, namespace="phIoT", doc="Fill level measurement")
LIGHT = TagDef(name="light", display_name="Light", kind=0, namespace="phIoT", doc="Related to lighting")
DISCHARGE = TagDef(
    name="discharge", display_name="Discharge", kind=0, namespace="phIoT", doc="Discharge side of equipment"
)
RETURN = TagDef(name="return", display_name="Return", kind=0, namespace="phIoT", doc="Return side of equipment")
SUPPLY = TagDef(name="supply", display_name="Supply", kind=0, namespace="phIoT", doc="Supply side of equipment")
MIXED = TagDef(name="mixed", display_name="Mixed", kind=0, namespace="phIoT", doc="Mixed air section")
OUTSIDE = TagDef(name="outside", display_name="Outside", kind=0, namespace="phIoT", doc="Outside or outdoor")
ZONE = TagDef(name="zone", display_name="Zone", kind=0, namespace="phIoT", doc="Conditioned zone")
ENTERING = TagDef(name="entering", display_name="Entering", kind=0, namespace="phIoT", doc="Entering pipe/duct")
LEAVING = TagDef(name="leaving", display_name="Leaving", kind=0, namespace="phIoT", doc="Leaving pipe/duct")
HOT = TagDef(name="hot", display_name="Hot", kind=0, namespace="phIoT", doc="Hot water or hot deck")
COLD = TagDef(name="cold", display_name="Cold", kind=0, namespace="phIoT", doc="Cold or chilled")
CONDENSER = TagDef(name="condenser", display_name="Condenser", kind=0, namespace="phIoT", doc="Condenser section")
EVAPORATOR = TagDef(name="evaporator", display_name="Evaporator", kind=0, namespace="phIoT", doc="Evaporator section")
DAMPER = TagDef(name="damper", display_name="Damper", kind=0, namespace="phIoT", doc="Damper actuator")
VALVE = TagDef(name="valve", display_name="Valve", kind=0, namespace="phIoT", doc="Valve actuator")
FAN = TagDef(name="fan", display_name="Fan", kind=0, namespace="phIoT", doc="Fan equipment or point")
PUMP = TagDef(name="pump", display_name="Pump", kind=0, namespace="phIoT", doc="Pump equipment or point")
FILTER = TagDef(name="filter", display_name="Filter", kind=0, namespace="phIoT", doc="Air or water filter")
RUN = TagDef(name="run", display_name="Run", kind=0, namespace="phIoT", doc="Run status or command")
ENABLE = TagDef(name="enable", display_name="Enable", kind=0, namespace="phIoT", doc="Enable status")
ALARM = TagDef(name="alarm", display_name="Alarm", kind=0, namespace="phIoT", doc="Alarm condition")
OCCUPIED = TagDef(name="occupied", display_name="Occupied", kind=0, namespace="phIoT", doc="Occupied mode")
AHU = TagDef(name="ahu", display_name="AHU", kind=0, namespace="phIoT", doc="Air Handling Unit")
VAV = TagDef(name="vav", display_name="VAV", kind=0, namespace="phIoT", doc="Variable Air Volume terminal unit")
FCU = TagDef(name="fcu", display_name="FCU", kind=0, namespace="phIoT", doc="Fan Coil Unit")
CHILLER = TagDef(name="chiller", display_name="Chiller", kind=0, namespace="phIoT", doc="Chiller plant")
BOILER = TagDef(name="boiler", display_name="Boiler", kind=0, namespace="phIoT", doc="Boiler plant")
COOLING_TOWER = TagDef(
    name="coolingTower", display_name="Cooling Tower", kind=0, namespace="phIoT", doc="Cooling tower"
)
METER = TagDef(name="meter", display_name="Meter", kind=0, namespace="phIoT", doc="Metering equipment")
UPS = TagDef(name="ups", display_name="UPS", kind=0, namespace="phIoT", doc="Uninterruptible Power Supply")
K_W = TagDef(name="kW", display_name="kW", kind=0, namespace="phIoT", doc="Kilowatts")
K_WH = TagDef(name="kWh", display_name="kWh", kind=0, namespace="phIoT", doc="Kilowatt-hours")
TOTAL = TagDef(name="total", display_name="Total", kind=0, namespace="phIoT", doc="Total or accumulated value")
NET = TagDef(name="net", display_name="Net", kind=0, namespace="phIoT", doc="Net value")
IMPORT = TagDef(name="import", display_name="Import", kind=0, namespace="phIoT", doc="Imported energy")
EXPORT = TagDef(name="export", display_name="Export", kind=0, namespace="phIoT", doc="Exported energy")
REACTIVE = TagDef(name="reactive", display_name="Reactive", kind=0, namespace="phIoT", doc="Reactive power/energy")
APPARENT = TagDef(name="apparent", display_name="Apparent", kind=0, namespace="phIoT", doc="Apparent power")
PHASE = TagDef(name="phase", display_name="Phase", kind=3, namespace="phIoT", doc="Electrical phase identifier")
SITE_REF = TagDef(name="siteRef", display_name="Site Ref", kind=4, namespace="phIoT", doc="Reference to parent site")
EQUIP_REF = TagDef(
    name="equipRef", display_name="Equip Ref", kind=4, namespace="phIoT", doc="Reference to parent equipment"
)
SPACE_REF = TagDef(
    name="spaceRef", display_name="Space Ref", kind=4, namespace="phIoT", doc="Reference to parent space"
)
FLOOR_REF = TagDef(name="floorRef", display_name="Floor Ref", kind=4, namespace="phIoT", doc="Reference to floor")
DEVICE_REF = TagDef(
    name="deviceRef", display_name="Device Ref", kind=4, namespace="phIoT", doc="Reference to gateway device"
)
DIS = TagDef(name="dis", display_name="Display Name", kind=3, namespace="ph", doc="Display name for the entity")
ID = TagDef(name="id", display_name="Identifier", kind=4, namespace="ph", doc="Unique identifier ref")
TZ = TagDef(name="tz", display_name="Timezone", kind=3, namespace="ph", doc="IANA timezone identifier")
GEO_ADDR = TagDef(name="geoAddr", display_name="Geo Address", kind=3, namespace="ph", doc="Geographic street address")
GEO_COORD = TagDef(name="geoCoord", display_name="Geo Coord", kind=9, namespace="ph", doc="Geographic coordinate")
AREA = TagDef(name="area", display_name="Area", kind=2, namespace="ph", doc="Floor area", unit_quantity="area")
UNIT = TagDef(name="unit", display_name="Unit", kind=3, namespace="ph", doc="Unit of measurement")
KIND = TagDef(name="kind", display_name="Kind", kind=3, namespace="ph", doc="Data kind")
HIS_INTERPOLATE = TagDef(
    name="hisInterpolate",
    display_name="His Interpolate",
    kind=3,
    namespace="phIoT",
    doc="History interpolation mode: COV, linear, break",
)

PACK = Vocabulary(
    name="core",
    version="1.0.0",
    tags=(
        SITE,
        BUILDING,
        FLOOR,
        SPACE,
        EQUIP,
        DEVICE,
        POINT,
        SENSOR,
        CMD,
        SP,
        HIS,
        WRITABLE,
        CUR,
        AIR,
        WATER,
        STEAM,
        ELEC,
        GAS,
        TEMP,
        HUMIDITY,
        PRESSURE,
        FLOW,
        CO2,
        POWER,
        ENERGY,
        VOLT,
        CURRENT,
        FREQ,
        PF,
        SPEED,
        LEVEL,
        LIGHT,
        DISCHARGE,
        RETURN,
        SUPPLY,
        MIXED,
        OUTSIDE,
        ZONE,
        ENTERING,
        LEAVING,
        HOT,
        COLD,
        CONDENSER,
        EVAPORATOR,
        DAMPER,
        VALVE,
        FAN,
        PUMP,
        FILTER,
        RUN,
        ENABLE,
        ALARM,
        OCCUPIED,
        AHU,
        VAV,
        FCU,
        CHILLER,
        BOILER,
        COOLING_TOWER,
        METER,
        UPS,
        K_W,
        K_WH,
        TOTAL,
        NET,
        IMPORT,
        EXPORT,
        REACTIVE,
        APPARENT,
        PHASE,
        SITE_REF,
        EQUIP_REF,
        SPACE_REF,
        FLOOR_REF,
        DEVICE_REF,
        DIS,
        ID,
        TZ,
        GEO_ADDR,
        GEO_COORD,
        AREA,
        UNIT,
        KIND,
        HIS_INTERPOLATE,
    ),
)
