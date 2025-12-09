from __future__ import annotations

from pydantic import BaseModel


class ProductionAsset(BaseModel):
    """
    Single line item in the Production Matrix (Module 4 simulation).
    """

    asset_name: str
    platform: str
    dimension: str
    asset_type: str
    creative_headline: str
    technical_notes: str


