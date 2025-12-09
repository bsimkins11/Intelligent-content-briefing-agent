from __future__ import annotations

"""
Matrix Engine – Production Matrix Generator (Module 4 simulation).

Takes a StrategySegment (Module 2) and CreativeConcept (Module 3), looks up
environment specs from SPEC_LIBRARY, and explodes them into a list of
ProductionAsset tickets (Module 4).
"""

from typing import List

from app.models.inputs import StrategySegment, CreativeConcept
from app.models.production_asset import ProductionAsset
from app.services.spec_library import SPEC_LIBRARY


def generate_bill_of_materials(strategy: StrategySegment, concept: CreativeConcept) -> List[ProductionAsset]:
    """
    Generate a Bill of Materials for production, given a strategy segment
    and a creative concept.
    """
    bill_of_materials: List[ProductionAsset] = []

    for env_id in strategy.selected_environments:
        spec = SPEC_LIBRARY.get(env_id)
        if not spec:
            continue

        platform = spec.get("platform", env_id)
        fmt = spec.get("format") or spec.get("format_name") or ""
        dimension = spec.get("dimension") or spec.get("dimensions") or ""
        allowed_types = spec.get("allowed_types") or []
        asset_type = allowed_types[0] if allowed_types else "STATIC"

        # Auto-generated taxonomy: Segment_Platform_Format_Concept
        safe_segment = strategy.segment_name.replace(" ", "")
        safe_platform = platform.replace(" ", "")
        safe_format = fmt.replace(" ", "")
        safe_concept = concept.concept_name.replace(" ", "")
        asset_name = f"{safe_segment}_{safe_platform}_{safe_format}_{safe_concept}"

        technical_notes_parts = []
        if spec.get("max_duration"):
            technical_notes_parts.append(f"Max duration: {spec['max_duration']}s")
        if spec.get("dimension"):
            technical_notes_parts.append(f"Dimension: {spec['dimension']}")
        if spec.get("is_html5_capable"):
            technical_notes_parts.append("HTML5 capable")

        technical_notes = "; ".join(technical_notes_parts) or "See spec library for full details."

        bill_of_materials.append(
            ProductionAsset(
                asset_name=asset_name,
                platform=platform,
                dimension=dimension,
                asset_type=asset_type,
                creative_headline=concept.master_headline or strategy.message_pillar,
                technical_notes=technical_notes,
            )
        )

    return bill_of_materials


