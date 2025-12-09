from __future__ import annotations

from typing import List

from pydantic import BaseModel


class StrategySegment(BaseModel):
    """
    Minimal representation of a Strategy card from Module 2
    for the Production Matrix simulation.
    """

    segment_name: str
    message_pillar: str
    selected_environments: List[str]


class CreativeConcept(BaseModel):
    """
    Minimal representation of a Concept card from Module 3
    for the Production Matrix simulation.
    """

    concept_name: str
    master_headline: str
    master_visual_path: str


