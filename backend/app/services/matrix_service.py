from __future__ import annotations

from typing import Dict, List

from app.schemas.brief import ModConBrief
from app.schemas.matrix import MatrixState, MessageRow


def _normalise_audience(name: str) -> str:
    return name.strip().lower()


def generate_matrix_draft(brief: ModConBrief) -> MatrixState:
    """
    POC-only generator: create a first-pass messaging row per audience.

    We do not call the LLM here to keep the demo fast and deterministic.
    Headlines and copy are templated from the SMP and audience names.
    """
    rows: List[MessageRow] = []

    smp = brief.smp or "Clarify the core promise for this campaign."
    base_cta = "Learn more"

    if not brief.audiences:
        # Single generic row when no explicit audiences have been captured yet.
        rows.append(
            MessageRow(
                id="MSG-001",
                audience_segment="Primary audience",
                headline=smp,
                body_copy=f"This message introduces the core idea: {smp}",
                cta=base_cta,
            )
        )
        return MatrixState(rows=rows)

    for idx, aud in enumerate(brief.audiences, start=1):
        seg = aud.strip() or f"Audience {idx}"
        row_id = f"MSG-{idx:03d}"
        headline = f"{smp} – for {seg}"
        body = (
            f"This variation explains the single-minded proposition for {seg}. "
            f"Emphasise why this audience cares most about: {smp}"
        )
        rows.append(
            MessageRow(
                id=row_id,
                audience_segment=seg,
                headline=headline,
                body_copy=body,
                cta=base_cta,
            )
        )

    return MatrixState(rows=rows)


def update_message_row(state: MatrixState, row_id: str, new_data: Dict) -> MatrixState:
    """
    Human override: replace a single row's fields with user-provided data.
    """
    updated_rows: List[MessageRow] = []
    for row in state.rows:
        if row.id == row_id:
            updated_rows.append(row.copy(update=new_data or {}))
        else:
            updated_rows.append(row)
    return MatrixState(rows=updated_rows)


def add_message_row(state: MatrixState, new_row_data: Dict) -> MatrixState:
    """
    Allow users to manually add a new audience/message row.

    If no explicit ID is provided, we auto-generate a simple MSG-XXX identifier.
    """
    existing_ids = [r.id for r in state.rows]
    auto_id = f"MSG-{len(existing_ids) + 1:03d}"

    row = MessageRow(
        id=new_row_data.get("id") or auto_id,
        audience_segment=new_row_data.get("audience_segment", "New audience"),
        headline=new_row_data.get("headline", "New headline"),
        body_copy=new_row_data.get("body_copy", ""),
        cta=new_row_data.get("cta", "Learn more"),
        status=new_row_data.get("status", "Draft"),
    )

    return MatrixState(rows=state.rows + [row])


