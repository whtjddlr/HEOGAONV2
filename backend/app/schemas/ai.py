from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class IntakeResult(BaseModel):
    intent: Literal["food", "signage", "outdoor", "general", "unsupported"] = "food"
    business_type: str | None = None
    region: str | None = None
    address: str | None = None
    building_use: str | None = None
    sales_modes: list[str] = Field(default_factory=list)
    signage_wanted: bool = False
    outdoor_wanted: bool = False
    liquor_sales: bool | None = None
    on_site_consumption: bool | None = None
    manufacturing_mode: str | None = None
    unknowns: list[str] = Field(default_factory=list)
    confidence: float = 0.0


class InquiryCandidate(BaseModel):
    title: str
    department: str
    reason: str = ""


class ConsultationAnalysis(BaseModel):
    summary: str
    resolved_items: list[str] = Field(default_factory=list)
    new_missing_fields: list[str] = Field(default_factory=list)
    new_inquiry_candidates: list[InquiryCandidate] = Field(default_factory=list)
    next_action: Literal["ask_followup", "inquiry", "documents", "dashboard"] = "dashboard"
    confidence: float = 0.0
