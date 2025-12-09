from typing import List

from pydantic import BaseModel


class MessageRow(BaseModel):
    """
    One row in the Audience & Messaging Matrix.

    For the POC, we keep the shape minimal and focused on copy:
      - audience_segment: who
      - headline / body_copy / cta: what
      - status: simple lifecycle flag for creative review
    """

    id: str
    audience_segment: str
    headline: str
    body_copy: str
    cta: str
    status: str = "Draft"


class MatrixState(BaseModel):
    rows: List[MessageRow] = []


