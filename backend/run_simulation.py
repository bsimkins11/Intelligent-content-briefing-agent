from __future__ import annotations

"""
Quick simulation script for the Production Matrix Engine (Module 4).

Scenario:
  - Strategy: "The Gamer" segment, targeting META_STORY, YT_BUMPER, DISPLAY_MPU
  - Concept:  "Level Up", headline "Play Faster."

Expected:
  - 3 production assets with distinct dimensions/specs/naming.
"""

import json

from app.models.inputs import StrategySegment, CreativeConcept
from app.services.matrix_engine import generate_bill_of_materials


def main() -> None:
  strategy = StrategySegment(
      segment_name="The Gamer",
      message_pillar="Speed and responsiveness matter most.",
      selected_environments=["META_STORY", "YT_BUMPER", "DISPLAY_MPU"],
  )

  concept = CreativeConcept(
      concept_name="Level Up",
      master_headline="Play Faster.",
      master_visual_path="/assets/concepts/level-up-master.jpg",
  )

  bom = generate_bill_of_materials(strategy, concept)
  print(json.dumps([asset.model_dump() for asset in bom], indent=2))


if __name__ == "__main__":
  main()


