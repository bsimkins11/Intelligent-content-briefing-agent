from typing import Any, Dict, List, Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.schemas.brief import ModConBrief
from app.services.brief_service import override_brief, update_brief_ai


router = APIRouter()


class BriefChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class BriefChatRequest(BaseModel):
    current_state: ModConBrief
    chat_log: List[BriefChatMessage]


class BriefChatResponse(BaseModel):
    reply: str
    state: ModConBrief


class BriefUpdateRequest(BaseModel):
    current_state: ModConBrief
    manual_updates: Dict[str, Any]


class BriefUpdateResponse(BaseModel):
    state: ModConBrief


@router.post("/chat", response_model=BriefChatResponse)
async def brief_chat(request: BriefChatRequest) -> BriefChatResponse:
    try:
        new_state, reply = update_brief_ai(
            current_state=request.current_state, chat_log=[m.dict() for m in request.chat_log]
        )
        return BriefChatResponse(reply=reply, state=new_state)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/update", response_model=BriefUpdateResponse)
async def brief_update(request: BriefUpdateRequest) -> BriefUpdateResponse:
    try:
        new_state = override_brief(
            current_state=request.current_state, manual_updates=request.manual_updates
        )
        return BriefUpdateResponse(state=new_state)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


