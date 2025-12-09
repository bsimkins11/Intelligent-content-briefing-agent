from __future__ import annotations

from typing import Dict, List

from app.schemas.brief import ModConBrief
from app.schemas.concepts import AssetComponent, ConceptState, CreativeConcept


def generate_concept_drafts(brief: ModConBrief) -> ConceptState:
    """
    POC-only: generate three lightweight visual directions from the brief.

    We keep this deterministic and template-based (no LLM) so the demo works
    reliably without requiring additional AI calls.
    """
    base_name = brief.campaign_name or "Modular Content System"
    smp = brief.smp or "Clarify the single-minded proposition."

    concepts: List[CreativeConcept] = []

    concepts.append(
        CreativeConcept(
            id="CON-101",
            name=f"{base_name} – Story Arc",
            visual_description=(
                "Vertical story showing the before/after of your primary audience. "
                f"Open on the problem, close on how the system delivers: {smp}."
            ),
            components=[
                AssetComponent(role="Background", asset_type="image"),
                AssetComponent(role="Primary Visual", asset_type="video"),
                AssetComponent(role="Logo Lockup", asset_type="image"),
            ],
        )
    )

    concepts.append(
        CreativeConcept(
            id="CON-102",
            name=f"{base_name} – System Overview",
            visual_description=(
                "Modular grid or dashboard-style graphic that breaks the offer into 3–4 tiles. "
                "Each tile highlights a core benefit aligned to the SMP."
            ),
            components=[
                AssetComponent(role="Background", asset_type="image"),
                AssetComponent(role="Icon Set", asset_type="image"),
            ],
        )
    )

    concepts.append(
        CreativeConcept(
            id="CON-103",
            name=f"{base_name} – Proof Carousel",
            visual_description=(
                "Carousel or multi-frame layout mixing product UI, people photography, and short proof points "
                "that ladder back to the single-minded proposition."
            ),
            components=[
                AssetComponent(role="Frame 1", asset_type="image"),
                AssetComponent(role="Frame 2", asset_type="image"),
                AssetComponent(role="Frame 3", asset_type="image"),
            ],
        )
    )

    return ConceptState(concepts=concepts)


def map_asset_to_component(
    state: ConceptState, concept_id: str, component_role: str, dam_url: str, dam_id: str | None = None
) -> ConceptState:
    """
    Human override: attach a specific DAM URL/ID to a component slot.
    """
    updated_concepts: List[CreativeConcept] = []

    for concept in state.concepts:
        if concept.id != concept_id:
            updated_concepts.append(concept)
            continue

        new_components: List[AssetComponent] = []
        for comp in concept.components:
            if comp.role == component_role:
                new_components.append(
                    AssetComponent(
                        role=comp.role,
                        asset_type=comp.asset_type,
                        dam_url=dam_url,
                        dam_id=dam_id or comp.dam_id,
                    )
                )
            else:
                new_components.append(comp)

        updated_concepts.append(
            CreativeConcept(
                id=concept.id,
                name=concept.name,
                visual_description=concept.visual_description,
                components=new_components,
            )
        )

    return ConceptState(concepts=updated_concepts)


def update_concept(state: ConceptState, concept_id: str, new_data: Dict) -> ConceptState:
    """
    Human override: edit concept name / description fields.
    """
    updated_concepts: List[CreativeConcept] = []
    for concept in state.concepts:
        if concept.id == concept_id:
            updated_concepts.append(concept.copy(update=new_data or {}))
        else:
            updated_concepts.append(concept)
    return ConceptState(concepts=updated_concepts)


