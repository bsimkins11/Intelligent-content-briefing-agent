import os
import json
from pathlib import Path
from typing import TypedDict, List

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage, BaseMessage, AIMessage
from langgraph.graph import StateGraph, END

# Load environment from backend/.env
ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=ENV_PATH, override=False)

_GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
_MODEL_NAME = os.getenv("GEMINI_MODEL", "models/gemini-2.5-pro")
_LLM_AVAILABLE = bool(_GOOGLE_API_KEY)

llm = (
    ChatGoogleGenerativeAI(
        model=_MODEL_NAME,
        temperature=0.4,  # balanced: concise but not overly rigid
        google_api_key=_GOOGLE_API_KEY,
    )
    if _LLM_AVAILABLE
    else None
)


class AgentState(TypedDict):
    messages: List[BaseMessage]
    current_plan: dict


SYSTEM_PROMPT = """You are an expert Content Strategy Architect and world-class ModCon briefing SME.
Your goal is to interview the user to build a "Production Master Plan" for an Intelligent Content Brief,
acting as the foundation for creative, media, and production teams.

The master plan is one object with two main parts:
1) A written creative brief (campaign story, objectives, audiences, SMP, constraints).
2) An execution layer (content matrix and bill of materials) that production teams can act on.

The structured plan includes:
- Core brief fields (campaign_name, single_minded_proposition, primary_audience, narrative_brief).
- Audience_matrix (rows describing segments, funnel stages, triggers, channels, notes).
- Channel_specs (per-channel / format specs and guardrails).
- Brand_voice and brand_visual_guidelines.
- Asset_libraries (references into a DAM or brand asset system).
- Bill_of_materials (asset-level requirements: id, format, concept, source_type, specs).
- Logic_map (if/then style rules for dynamic assembly).
- Content_matrix (rows combining asset_id + audience_segment + stage + trigger + channel + format + message + variant + notes).
- Custom brief fields: honor any extra fields provided by the user and update them as you learn more.

Your process:
- Phase 1 (Briefing): Act as a consultant. Ask clarifying questions one step at a time to co-write the narrative brief and fill in core fields.
- Use any uploaded audience matrix information explicitly (refer to segments, triggers, etc.).
- When the user indicates the brief feels solid, summarise it back as a clean narrative_brief and confirm.
- Phase 2 (Content Matrix): Propose a first pass content_matrix based on the brief, audience_matrix, and channel_specs.
- Think in terms of audience x funnel_stage x trigger x channel, and map rows to asset concepts in the bill_of_materials.
- Suggest sample concepts and labels for variants that a creative director could react to.
- Be explicit and useful for downstream teams (creative, media, production). Flag gaps, mandatories, and assumptions.
- The agent can be adapted with company-specific context later; note any places where brand data or historical learnings would help.

Current Plan State:
{current_plan}
"""


def call_model(state: AgentState):
    messages = state["messages"]
    current_plan_str = json.dumps(state.get("current_plan", {}), indent=2)
    system_msg = SystemMessage(content=SYSTEM_PROMPT.format(current_plan=current_plan_str))

    # Stub mode
    if os.getenv("DEMO_AGENT_STUB") == "1":
        stub_reply = (
            "Demo mode: let's lock a solid ModCon brief. Give me campaign name, SMP, primary audience, "
            "KPIs, flight dates, mandatories, tone, offers, proof points, and any brand assets. "
            "If you share an audience matrix or specs, I'll shape the content matrix next. "
            "Quality: 3/10. Gaps: missing SMP, audiences, KPIs, mandatories, tone."
        )
        return {"messages": [AIMessage(content=stub_reply)]}

    if not _LLM_AVAILABLE or llm is None:
        fallback = (
            "I can't reach Gemini because the API key isn't loaded. Please set GOOGLE_API_KEY and restart the server. "
            "Share campaign name, SMP, audiences, KPIs, flight dates, mandatories, tone/voice, offers, proof points, "
            "and specs/asset libraries, and I'll draft the brief once connected."
        )
        return {"messages": [AIMessage(content=fallback)]}

    try:
        response = llm.invoke([system_msg] + messages)
        return {"messages": [response]}
    except Exception as exc:
        fallback = (
            "I hit an issue reaching the model. Let's keep going anyway: share campaign name, SMP, "
            "primary audience(s), KPIs, flight dates, mandatories, tone/voice, offers, proof points, "
            "and any specs/asset libraries. I'll draft a ModCon brief and content matrix from that."
        )
        return {"messages": [AIMessage(content=f"{fallback} (error: {exc})")]}


def should_continue(state: AgentState):
    return END


workflow = StateGraph(AgentState)
workflow.add_node("agent", call_model)
workflow.set_entry_point("agent")
workflow.add_edge("agent", END)
app_graph = workflow.compile()


async def process_message(history: List[dict], current_plan: dict):
    lc_messages: List[BaseMessage] = []
    for msg in history:
        if msg.get("role") == "user":
            lc_messages.append(HumanMessage(content=msg.get("content", "")))
        else:
            lc_messages.append(AIMessage(content=msg.get("content", "")))

    inputs = {"messages": lc_messages, "current_plan": current_plan}
    result = await app_graph.ainvoke(inputs)
    last_msg = result["messages"][-1]
    return last_msg.content
