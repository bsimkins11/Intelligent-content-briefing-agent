from typing import List

from fastapi import APIRouter, HTTPException

from app.schemas.specs import Spec, SpecCreate
from app.services.spec_service import get_all_specs, save_spec


router = APIRouter()


@router.get("", response_model=List[Spec])
async def list_specs() -> List[Spec]:
    """
    Return the current spec library for use in dropdowns and planning tools.
    """
    try:
        return get_all_specs()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("", response_model=Spec)
async def create_spec(payload: SpecCreate) -> Spec:
    """
    Create a new custom spec (POC-only: stored in JSON).
    """
    try:
        return save_spec(payload)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


