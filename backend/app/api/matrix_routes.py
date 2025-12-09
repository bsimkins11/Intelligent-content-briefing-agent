from typing import Any, Dict

from fastapi import APIRouter, HTTPException, Path
from pydantic import BaseModel

from app.schemas.brief import ModConBrief
from app.schemas.matrix import MatrixState, MessageRow
from app.services.matrix_service import add_message_row, generate_matrix_draft, update_message_row


router = APIRouter()


class GenerateMatrixRequest(BaseModel):
    brief: ModConBrief


class GenerateMatrixResponse(BaseModel):
    state: MatrixState


class UpdateRowRequest(BaseModel):
    state: MatrixState
    new_data: Dict[str, Any]


class UpdateRowResponse(BaseModel):
    state: MatrixState


class AddRowRequest(BaseModel):
    state: MatrixState
    row: Dict[str, Any]


class AddRowResponse(BaseModel):
    state: MatrixState


@router.post("/generate", response_model=GenerateMatrixResponse)
async def generate_matrix(request: GenerateMatrixRequest) -> GenerateMatrixResponse:
    try:
        state = generate_matrix_draft(request.brief)
        return GenerateMatrixResponse(state=state)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/row/{row_id}", response_model=UpdateRowResponse)
async def update_row(
    request: UpdateRowRequest, row_id: str = Path(..., description="ID of the message row to update")
) -> UpdateRowResponse:
    try:
        state = update_message_row(state=request.state, row_id=row_id, new_data=request.new_data)
        return UpdateRowResponse(state=state)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/add-row", response_model=AddRowResponse)
async def add_row(request: AddRowRequest) -> AddRowResponse:
    try:
        state = add_message_row(state=request.state, new_row_data=request.row)
        return AddRowResponse(state=state)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


