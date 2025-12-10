from __future__ import annotations

from typing import List

from pydantic import BaseModel


class DeliveryDestination(BaseModel):
    """
    One downstream delivery endpoint for a master production asset.
    """

    platform_name: str  # e.g., "TikTok"
    spec_id: str  # Reference into the spec library / environment ID
    format_name: str  # e.g., "In-Feed Video"
    special_notes: str  # e.g., "Strict Safe Zone bottom 150px"


class ProductionJob(BaseModel):
    """
    Represents ONE unique asset to be produced, which may serve multiple partners.

    This is the Many-to-One "master ticket" that collapses redundant specs
    (e.g., TikTok + Reels + Shorts all using the same 9:16 master edit).
    """

    job_id: str  # e.g., "JOB-2025-001"
    creative_concept: str  # e.g., "Summer Sale - High Energy"
    asset_type: str  # e.g., "Vertical Video (9:16)"

    # Grouped downstream endpoints that share this master asset
    destinations: List[DeliveryDestination]

    # Production + operational metadata
    technical_summary: str  # e.g., "1080x1920, 15s, MP4"
    status: str = "Pending"  # Pending, In-Production, Approved, Delivered
    source_type: str | None = None  # e.g., "New Shoot", "Stock", "Reuse"
    shoot_code: str | None = None  # Link to shoot or kit (e.g., "SHOOT-ABC-2025")
    version_tag: str | None = None  # e.g., "v1", "v1.1_localized"
    owner: str | None = None  # Producer / editor responsible
    due_date: str | None = None  # ISO date string for POC
    round_label: str | None = None  # e.g., "R1", "R2", "Final"
    asset_feed_row_ids: list[str] | None = None  # Optional linkage into the asset feed


