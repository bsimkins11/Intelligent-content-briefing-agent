from __future__ import annotations

import json
from typing import Any, Dict, List, Tuple

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from app.agent_core import llm
from app.schemas.brief import ModConBrief


SYSTEM_PROMPT = """
You are helping a strategist co-write a modular content brief called a ModConBrief.

You receive:
- current_state: the existing ModConBrief as JSON
- chat_log: the full conversation between user and assistant so far

Your job:
1) Reply conversationally to the user as an expert creative strategist.
2) Update the ModConBrief fields (campaign_name, smp, audiences, kpis, flight_dates, status)
   based on the new information in the chat.

IMPORTANT OUTPUT FORMAT:
Return ONLY valid JSON with this exact shape and no extra commentary:
{{
  "assistant_reply": "natural language reply to the user",
  "modcon_brief": {{
    "campaign_name": "...",
    "smp": "...",
    "audiences": ["..."],
    "kpis": ["..."],
    "flight_dates": {{"start": "...", "end": "..."}},
    "status": "Draft"  // or "Approved"
  }}
}}
"""


def update_brief_ai(current_state: ModConBrief, chat_log: List[Dict[str, str]]) -> Tuple[ModConBrief, str]:
    """
    Use the shared Gemini LLM to update the ModConBrief from chat.

    This stays deliberately thin: it lets the model propose an updated brief
    and a conversational reply, then we validate & merge the state.
    """
    system = SystemMessage(
        content=SYSTEM_PROMPT.format(current_state=current_state.model_dump())
    )

    messages = [system]
    for msg in chat_log:
        role = msg.get("role")
        content = msg.get("content", "")
        if not content:
            continue
        if role == "user":
            messages.append(HumanMessage(content=content))
        else:
            messages.append(AIMessage(content=content))

    response = llm.invoke(messages)
    raw = response.content if isinstance(response, AIMessage) else str(response)

    try:
        payload = json.loads(raw)
    except Exception:
        # Fallback: keep state, surface raw text as the reply
        return current_state, raw

    assistant_reply = str(payload.get("assistant_reply", "")).strip() or raw

    brief_data = payload.get("modcon_brief") or {}
    try:
        updated = current_state.copy(update=brief_data)
    except Exception:
        updated = current_state

    return updated, assistant_reply


def override_brief(current_state: ModConBrief, manual_updates: Dict[str, Any]) -> ModConBrief:
    """
    Human override: apply direct edits onto the ModConBrief.

    In case of conflict between AI and human, the human wins.
    """
    return current_state.copy(update=manual_updates or {})


