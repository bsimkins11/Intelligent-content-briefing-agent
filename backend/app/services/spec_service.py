from __future__ import annotations

import json
import os
from typing import List

from app.schemas.specs import Spec, SpecCreate


def _specs_path() -> str:
    here = os.path.dirname(__file__)
    return os.path.join(here, "..", "data", "specs.json")


def get_all_specs() -> List[Spec]:
    """
    Return the full spec library from the JSON file.
    """
    path = _specs_path()
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    return [Spec(**item) for item in raw]


def save_spec(spec_data: SpecCreate) -> Spec:
    """
    Append a new spec to the JSON file (POC-only; no concurrency control).
    """
    path = _specs_path()
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    specs = [Spec(**item) for item in raw]

    # Auto-generate an ID if not provided.
    if spec_data.id:
        new_id = spec_data.id
    else:
        base = f"{spec_data.platform}_{spec_data.placement}".upper().replace(" ", "_")
        new_id = base
        existing_ids = {s.id for s in specs}
        suffix = 1
        while new_id in existing_ids:
            new_id = f"{base}_{suffix}"
            suffix += 1

    new_spec = Spec(id=new_id, **spec_data.model_dump(exclude={"id"}))
    specs.append(new_spec)

    with open(path, "w", encoding="utf-8") as f:
        json.dump([s.model_dump() for s in specs], f, indent=2)

    return new_spec


