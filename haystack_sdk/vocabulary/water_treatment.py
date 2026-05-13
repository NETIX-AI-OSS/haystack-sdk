"""AUTO-GENERATED from haystack_sdk/vocabulary/data/water_treatment_tags.json — DO NOT EDIT BY HAND.

Regenerate with::

    python scripts/generate_vocabulary.py
"""

from __future__ import annotations

from haystack_sdk.vocabulary._base import TagDef, Vocabulary

WATER_TREATMENT_PLANT = TagDef(
    name="waterTreatmentPlant",
    display_name="Water Treatment Plant",
    kind=0,
    namespace="netix",
    doc="Site is a water treatment or wastewater treatment facility",
)
TREATMENT_BASIN = TagDef(
    name="treatmentBasin",
    display_name="Treatment Basin",
    kind=0,
    namespace="netix",
    doc="Sedimentation or primary filtration basin",
)
CLARIFIER = TagDef(
    name="clarifier",
    display_name="Clarifier",
    kind=0,
    namespace="netix",
    doc="Clarification vessel for coagulation and flocculation",
)
AERATION_TANK = TagDef(
    name="aerationTank",
    display_name="Aeration Tank",
    kind=0,
    namespace="netix",
    doc="Aeration tank or bioreactor for biological treatment",
)
UV_STERILIZER = TagDef(
    name="uvSterilizer",
    display_name="UV Sterilizer",
    kind=0,
    namespace="netix",
    doc="UV sterilization unit for disinfection",
)
MEMBRANE_FILTER = TagDef(
    name="membraneFilter",
    display_name="Membrane Filter",
    kind=0,
    namespace="netix",
    doc="Reverse osmosis or ultrafiltration membrane module",
)
CHEMICAL_DOSING_UNIT = TagDef(
    name="chemicalDosingUnit",
    display_name="Chemical Dosing Unit",
    kind=0,
    namespace="netix",
    doc="Chemical dosing system for chlorination, pH correction, or coagulant addition",
)
WATER_QUALITY_SENSOR = TagDef(
    name="waterQualitySensor",
    display_name="Water Quality Sensor",
    kind=0,
    namespace="netix",
    doc="Inline multi-parameter water quality sensor (turbidity, pH, chlorine, conductivity)",
)

WATER_TREATMENT = Vocabulary(
    name="water_treatment",
    version="1.0.0",
    tags=(
        WATER_TREATMENT_PLANT,
        TREATMENT_BASIN,
        CLARIFIER,
        AERATION_TANK,
        UV_STERILIZER,
        MEMBRANE_FILTER,
        CHEMICAL_DOSING_UNIT,
        WATER_QUALITY_SENSOR,
    ),
)
