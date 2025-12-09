from enum import Enum
from typing import Dict, List

from pydantic import BaseModel


class BriefStatus(str, Enum):
    DRAFT = "Draft"
    APPROVED = "Approved"


class ModConBrief(BaseModel):
    """
    Lightweight state object for the ModCon Brief engine.

    This intentionally overlaps with parts of the existing ProductionMasterPlan
    without trying to replace it. Think of it as the "front door" brief that
    can later be projected into the richer ProductionMasterPlan schema.
    """

    campaign_name: str = ""
    smp: str = ""
    audiences: List[str] = []
    kpis: List[str] = []
    flight_dates: Dict[str, str] = {}
    status: BriefStatus = BriefStatus.DRAFT


