from typing import List, Optional

from pydantic import BaseModel


class AssetComponent(BaseModel):
    """One visual component in a concept, typically mapped to a DAM asset."""

    role: str  # e.g. "Background", "Primary Visual", "Logo Lockup"
    asset_type: str  # e.g. "image", "video", "logo"
    dam_url: Optional[str] = None
    dam_id: Optional[str] = None


class CreativeConcept(BaseModel):
    """A modular creative concept that can be wired into assets later."""

    id: str
    name: str
    visual_description: str
    components: List[AssetComponent] = []


class ConceptState(BaseModel):
    concepts: List[CreativeConcept] = []


