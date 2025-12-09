from typing import Any, Dict

from pydantic import BaseModel


class Spec(BaseModel):
    id: str
    platform: str
    placement: str
    width: int
    height: int
    orientation: str
    media_type: str
    notes: str | None = None


class SpecCreate(BaseModel):
    platform: str
    placement: str
    width: int
    height: int
    orientation: str
    media_type: str
    notes: str | None = None
    id: str | None = None


