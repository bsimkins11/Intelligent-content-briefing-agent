from typing import List, Dict

from pydantic import BaseModel, Field
from typing_extensions import Literal


class StrategicMatrixRow(BaseModel):
    """
    A single row in the Decision Table.
    Maps WHO (Signal) -> WHY (Strategy) -> WHAT (Creative Directive).
    """

    # --- SECTION A: THE SIGNAL (Who & When) ---
    # These fields define the "IF" condition for the DCO logic.

    segment_id: str = Field(
        ...,
        description="Unique identifier for the audience persona (e.g., 'urban_millennial_pro').",
    )

    lifecycle_stage: Literal[
        "awareness", "consideration", "conversion", "retention", "win_back"
    ] = Field(
        ...,
        description="Where the user currently sits in the customer journey.",
    )

    context_trigger: str = Field(
        ...,
        description=(
            "The real-world data signal triggering this content "
            "(e.g., 'Rainy Weather', 'Cart Abandoned > 24h', 'Competitor Keyword Search')."
        ),
    )

    # --- SECTION B: THE HOOK (Psychology & Strategy) ---
    # These fields guide the AI or Copywriter on HOW to persuade.

    psych_driver: str = Field(
        ...,
        description=(
            "The primary psychological lever (e.g., 'Loss Aversion', 'Social Proof', "
            "'Authority', 'Instant Gratification')."
        ),
    )

    emotional_tone: str = Field(
        ...,
        description=(
            "The required mood/tone of the creative "
            "(e.g., 'Urgent', 'Empathetic', 'Confident', 'Playful')."
        ),
    )

    buying_barrier: str = Field(
        ...,
        description=(
            "The specific hesitation this asset must overcome "
            "(e.g., 'Price Sensitivity', 'Trust/Safety', 'Complexity')."
        ),
    )

    # --- SECTION C: THE PAYLOAD (Creative Directives) ---
    # These fields dictate the components of the master asset.

    visual_archetype: str = Field(
        ...,
        description=(
            "Description of the visual style required "
            "(e.g., 'UGC-style selfie video', 'High-gloss product macro', 'Kinetic typography')."
        ),
    )

    messaging_angle: str = Field(
        ...,
        description=(
            "The strategic focus of the copy (e.g., 'Focus on speed of delivery', "
            "'Focus on durability'). NOT the final copy text."
        ),
    )

    dynamic_elements: List[str] = Field(
        ...,
        description=(
            "List of specific elements that must be swappable "
            "(e.g., ['City Name', 'Discount %', 'Weather Icon'])."
        ),
    )


class AudienceContentMatrix(BaseModel):
    """
    The full output object containing the list of strategic decisions.
    """

    campaign_name: str
    decision_rows: List[StrategicMatrixRow]


