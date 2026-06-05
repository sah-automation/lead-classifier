from fastapi import APIRouter, HTTPException

from models.lead import ClassifyRequest, ClassifyResponse
from services.gemini_service import classify_lead

router = APIRouter(tags=["Classification"])


@router.post("/classify", response_model=ClassifyResponse)
def classify_message(payload: ClassifyRequest):
    """Classify a lead message and generate a suggested reply."""
    result = classify_lead(payload.message)

    if not result.get("classification") or not result.get("suggested_reply"):
        raise HTTPException(
            status_code=500,
            detail="Failed to classify message."
        )

    return ClassifyResponse(
        classification=result["classification"],
        suggested_reply=result["suggested_reply"],
    )