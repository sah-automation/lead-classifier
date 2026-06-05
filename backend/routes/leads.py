from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query

from models.lead import LeadCreate, LeadResponse, LeadUpdateContacted
from services.gemini_service import classify_lead
from services.lead_service import (
    get_all_leads,
    get_lead_by_id,
    insert_lead,
    update_contacted_status,
)

router = APIRouter(tags=["Leads"])


@router.post("/lead", response_model=LeadResponse, status_code=201)
def create_lead(payload: LeadCreate):
    """Create a new lead, classify it with Gemini, and store it."""
    result = classify_lead(payload.message)

    lead_id = insert_lead(
        lead=payload,
        classification=result["classification"],
        suggested_reply=result["suggested_reply"],
    )

    created_lead = get_lead_by_id(lead_id)
    if not created_lead:
        raise HTTPException(
            status_code=500,
            detail="Lead was created but could not be retrieved."
        )

    return created_lead


@router.get("/leads", response_model=List[LeadResponse])
def list_leads(classification: Optional[str] = Query(default=None)):
    """Return all leads, optionally filtered by classification."""
    allowed = {"Hot", "Warm", "Cold"}

    if classification and classification not in allowed:
        raise HTTPException(
            status_code=400,
            detail="classification must be one of: Hot, Warm, Cold"
        )

    return get_all_leads(classification=classification)


@router.patch("/lead/{lead_id}/contacted", response_model=LeadResponse)
def mark_as_contacted(lead_id: int, payload: LeadUpdateContacted):
    """Update contacted status for a specific lead."""
    updated = update_contacted_status(lead_id, payload.contacted)

    if not updated:
        raise HTTPException(status_code=404, detail="Lead not found.")

    lead = get_lead_by_id(lead_id)
    if not lead:
        raise HTTPException(
            status_code=404,
            detail="Lead not found after update."
        )

    return lead