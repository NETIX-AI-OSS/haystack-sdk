"""AUTO-GENERATED from haystack_sdk/vocabulary/data/fdd_tags.json — DO NOT EDIT BY HAND.

Regenerate with::

    python scripts/generate_vocabulary.py
"""

from __future__ import annotations

from haystack_sdk.vocabulary._base import TagDef, Vocabulary

EQUIP_TYPE = TagDef(
    name="equipType",
    display_name="Equipment Type",
    kind=3,
    namespace="netix",
    doc="FDD equipment class name (e.g. AHU, FAHU, FCU, Chiller). Used by the alarm rule template engine to scope point lookups to a specific equipment class.",
)
FDD_TAG_NAME = TagDef(
    name="fddTagName",
    display_name="FDD Tag Name",
    kind=3,
    namespace="netix",
    doc="Canonical point name from the NETIX equipment template (e.g. 'Supply Air Temperature'). The FDD alarm rule template engine resolves AlarmRuleTemplate.tag_name to tag_id by querying PointTagDict where fddTagName matches.",
)
RUN_HOURS = TagDef(
    name="runHours",
    display_name="Run Hours",
    kind=0,
    namespace="netix",
    doc="Point tracks cumulative equipment run-hours",
)

FDD = Vocabulary(
    name="fdd",
    version="1.0.0",
    tags=(
        EQUIP_TYPE,
        FDD_TAG_NAME,
        RUN_HOURS,
    ),
)
