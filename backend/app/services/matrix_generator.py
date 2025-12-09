from __future__ import annotations

"""
Module 4 – Production Matrix generator.

Takes a Strategy row (Module 2) and a Concept (Module 3), looks up specs from
the SPEC_LIBRARY, and generates a set of ProductionAsset tickets (Module 4).
"""

from typing import List, Tuple

from app.models.production_matrix import ProductionAsset, ProductionBatch
from app.schemas.concepts import CreativeConcept
from app.schemas.strategic_matrix import StrategicMatrixRow
from app.services.spec_library import get_spec_by_id


# In-memory stores for the POC (no real database yet).
_BATCHES: dict[str, ProductionBatch] = {}
_ASSETS: dict[str, ProductionAsset] = {}


def _normalize_environment_ids(raw_envs: List[str]) -> List[str]:
    """
    POC-friendly normalisation for platform_environments.

    The Strategy Matrix may store human-readable labels
    (e.g. 'Meta: Stories/Reels (9:16)'), but the SPEC_LIBRARY is keyed
    by environment IDs like 'META_STORY'.

    This helper maps fuzzy labels to the closest spec IDs and falls back
    to a sensible demo set if nothing matches.
    """
    normalized: List[str] = []

    for raw in raw_envs:
        label = (raw or "").strip()
        upper = label.upper()

        if not label:
            continue

        # Direct ID pass-through
        if upper in {"META_STORY", "META_FEED", "YT_BUMPER", "DISPLAY_MPU", "DISPLAY_LEADER"}:
            normalized.append(upper)
            continue

        # Fuzzy mappings based on common copy in the UI / strategist language
        if "STOR" in upper or "REEL" in upper:
            normalized.append("META_STORY")
            continue

        if "FEED" in upper and "META" in upper:
            normalized.append("META_FEED")
            continue

        if "BUMPER" in upper or "6S" in upper or ("YOUTUBE" in upper and "16:9" in upper):
            normalized.append("YT_BUMPER")
            continue

        if "300X250" in upper or "MPU" in upper:
            normalized.append("DISPLAY_MPU")
            continue

        if "728X90" in upper or "LEADER" in upper:
            normalized.append("DISPLAY_LEADER")
            continue

    # Deduplicate while preserving order
    seen: set[str] = set()
    deduped: List[str] = []
    for eid in normalized:
        if eid not in seen:
            seen.add(eid)
            deduped.append(eid)

    # POC safety net: if after normalisation we still have nothing,
    # return a small default pack so the board is never empty.
    if not deduped:
        return ["META_STORY", "YT_BUMPER", "DISPLAY_MPU"]

    return deduped


def generate_production_plan(
    campaign_id: str,
    strategy: StrategicMatrixRow,
    concept: CreativeConcept,
    batch_name: str | None = None,
    source_asset_requirements: str | None = None,
    adaptation_instruction: str | None = None,
) -> Tuple[ProductionBatch, List[ProductionAsset]]:
    """
    Core 'explosion' logic for the Production Matrix.

    - Reads `platform_environments` from the Strategy row (e.g. ['META_STORY', 'DISPLAY_MPU']).
    - For each environment ID, looks up a spec in SPEC_LIBRARY.
    - Creates a ProductionAsset ticket with spec + directive context.
    """
    raw_envs = strategy.platform_environments or []
    env_ids = _normalize_environment_ids(raw_envs)

    batch = ProductionBatch(
        campaign_id=campaign_id,
        strategy_segment_id=strategy.segment_id,
        concept_id=concept.id,
        batch_name=batch_name or f"{strategy.segment_name} – {concept.name}",
    )
    _BATCHES[batch.id] = batch

    assets: List[ProductionAsset] = []

    for env_id in env_ids:
        spec = get_spec_by_id(env_id)
        if not spec:
            continue

        platform = spec.get("platform", env_id)
        placement = spec.get("placement", spec.get("format_name", ""))
        dimensions = spec.get("dimensions", "")
        asset_type = spec.get("asset_type", "static")

        # Simple auto-generated name: Segment_Platform_Placement
        safe_segment = strategy.segment_name.replace(" ", "") or strategy.segment_id
        safe_platform = platform.replace(" ", "")
        safe_place = placement.replace(" ", "")
        asset_name = f"{safe_segment}_{safe_platform}_{safe_place}"

        asset = ProductionAsset(
            batch_id=batch.id,
            asset_name=asset_name,
            platform=platform,
            placement=placement,
            spec_dimensions=dimensions,
            spec_details=spec,
            asset_type=asset_type,
            visual_directive=concept.visual_description,
            copy_headline=strategy.primary_message_pillar,
            source_asset_requirements=source_asset_requirements,
            adaptation_instruction=adaptation_instruction,
        )

        _ASSETS[asset.id] = asset
        assets.append(asset)

    return batch, assets


def get_batch(batch_id: str) -> tuple[ProductionBatch | None, List[ProductionAsset]]:
    """
    Retrieve a ProductionBatch and all associated assets.
    """
    batch = _BATCHES.get(batch_id)
    if not batch:
        return None, []

    assets = [a for a in _ASSETS.values() if a.batch_id == batch_id]
    return batch, assets


def update_asset_status(asset_id: str, status: str) -> ProductionAsset | None:
    """
    Update the workflow status of a given ProductionAsset.
    """
    asset = _ASSETS.get(asset_id)
    if not asset:
        return None
    asset.status = status
    _ASSETS[asset_id] = asset
    return asset


