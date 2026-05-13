"""AUTO-GENERATED from haystack_sdk/vocabulary/data/retail_mall_tags.json — DO NOT EDIT BY HAND.

Regenerate with::

    python scripts/generate_vocabulary.py
"""

from __future__ import annotations

from haystack_sdk.vocabulary._base import TagDef, Vocabulary

RETAIL_MALL = TagDef(
    name="retailMall", display_name="Retail Mall", kind=0, namespace="netix", doc="Site is a retail shopping mall"
)
TENANT_UNIT = TagDef(
    name="tenantUnit",
    display_name="Tenant Unit",
    kind=0,
    namespace="netix",
    doc="Space is a leasable retail unit within a mall",
)
FASHION_TENANT = TagDef(
    name="fashionTenant",
    display_name="Fashion Tenant",
    kind=0,
    namespace="netix",
    doc="Tenant operates a clothing or apparel store",
)
FOOTWEAR_TENANT = TagDef(
    name="footwearTenant",
    display_name="Footwear Tenant",
    kind=0,
    namespace="netix",
    doc="Tenant operates a footwear or shoe store",
)
SPORTS_TENANT = TagDef(
    name="sportsTenant",
    display_name="Sports Tenant",
    kind=0,
    namespace="netix",
    doc="Tenant operates a sports or activewear store",
)
F_AND_BTENANT = TagDef(
    name="fAndBTenant",
    display_name="F&B Tenant",
    kind=0,
    namespace="netix",
    doc="Tenant operates a food and beverage outlet (restaurant, café, fast food)",
)
BEAUTY_TENANT = TagDef(
    name="beautyTenant",
    display_name="Beauty Tenant",
    kind=0,
    namespace="netix",
    doc="Tenant operates a beauty, cosmetics, or personal care store",
)
ELECTRONICS_TENANT = TagDef(
    name="electronicsTenant",
    display_name="Electronics Tenant",
    kind=0,
    namespace="netix",
    doc="Tenant operates an electronics or technology store",
)
SERVICES_TENANT = TagDef(
    name="servicesTenant",
    display_name="Services Tenant",
    kind=0,
    namespace="netix",
    doc="Tenant operates a service business: bank, telecom, salon, pharmacy, or similar",
)
KIDS_RETAIL_TENANT = TagDef(
    name="kidsRetailTenant",
    display_name="Kids Retail Tenant",
    kind=0,
    namespace="netix",
    doc="Tenant operates a children's goods or clothing store",
)
JEWELRY_TENANT = TagDef(
    name="jewelryTenant",
    display_name="Jewelry Tenant",
    kind=0,
    namespace="netix",
    doc="Tenant operates a jewelry, watch, or fine accessories store",
)
HOME_LIVING_TENANT = TagDef(
    name="homeLivingTenant",
    display_name="Home & Living Tenant",
    kind=0,
    namespace="netix",
    doc="Tenant operates a home goods, kitchenware, or interior store",
)
TENANT_METER = TagDef(
    name="tenantMeter",
    display_name="Tenant Meter",
    kind=0,
    namespace="netix",
    doc="Electrical sub-meter scoped to a single tenant unit",
)
SWITCHBOARD = TagDef(
    name="switchboard",
    display_name="Switchboard",
    kind=0,
    namespace="netix",
    doc="Main electrical distribution switchboard (ВРУ/WRU in CIS convention); feeds one or more tenant zones",
)
TRANSFORMER_PANEL = TagDef(
    name="transformerPanel",
    display_name="Transformer Panel",
    kind=0,
    namespace="netix",
    doc="Transformer substation distribution panel (TP); feeds one or more switchboards",
)

RETAIL_MALL = Vocabulary(
    name="retail_mall",
    version="1.0.0",
    tags=(
        RETAIL_MALL,
        TENANT_UNIT,
        FASHION_TENANT,
        FOOTWEAR_TENANT,
        SPORTS_TENANT,
        F_AND_BTENANT,
        BEAUTY_TENANT,
        ELECTRONICS_TENANT,
        SERVICES_TENANT,
        KIDS_RETAIL_TENANT,
        JEWELRY_TENANT,
        HOME_LIVING_TENANT,
        TENANT_METER,
        SWITCHBOARD,
        TRANSFORMER_PANEL,
    ),
)
