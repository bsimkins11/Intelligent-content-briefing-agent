from typing import Any, Dict

from fastapi import APIRouter, HTTPException, Path
from pydantic import BaseModel

from app.schemas.brief import ModConBrief
from app.schemas.concepts import ConceptState, CreativeConcept
from app.services.concept_service import (
    generate_concept_drafts,
    map_asset_to_component,
    update_concept,
)


router = APIRouter()


class GenerateConceptsRequest(BaseModel):
    brief: ModConBrief


class GenerateConceptsResponse(BaseModel):
    state: ConceptState


class UpdateConceptRequest(BaseModel):
    state: ConceptState
    new_data: Dict[str, Any]


class UpdateConceptResponse(BaseModel):
    state: ConceptState


class UpdateAssetsRequest(BaseModel):
    state: ConceptState
    component_role: str
    dam_url: str
    dam_id: str | None = None


class UpdateAssetsResponse(BaseModel):
    state: ConceptState


@router.post("/generate", response_model=GenerateConceptsResponse)
async def generate_concepts(request: GenerateConceptsRequest) -> GenerateConceptsResponse:
    try:
        state = generate_concept_drafts(request.brief)
        return GenerateConceptsResponse(state=state)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{concept_id}", response_model=UpdateConceptResponse)
async def edit_concept(
    request: UpdateConceptRequest,
    concept_id: str = Path(..., description="ID of the concept to update"),
) -> UpdateConceptResponse:
    try:
        state = update_concept(request.state, concept_id=concept_id, new_data=request.new_data)
        return UpdateConceptResponse(state=state)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{concept_id}/assets", response_model=UpdateAssetsResponse)
async def edit_concept_assets(
    request: UpdateAssetsRequest,
    concept_id: str = Path(..., description="ID of the concept to update components for"),
) -> UpdateAssetsResponse:
    try:
        state = map_asset_to_component(
            state=request.state,
            concept_id=concept_id,
            component_role=request.component_role,
            dam_url=request.dam_url,
            dam_id=request.dam_id,
        )
        return UpdateAssetsResponse(state=state)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


