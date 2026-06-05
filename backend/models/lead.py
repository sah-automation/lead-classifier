from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


# --- Input Models ---

class LeadCreate(BaseModel):
    """Input schema for POST /lead"""
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=20)
    message: str = Field(..., min_length=1)
    source: Optional[str] = Field(None, max_length=50)  # e.g. "website", "whatsapp", "email"


class ClassifyRequest(BaseModel):
    """Input schema for POST /classify"""
    message: str = Field(..., min_length=1)


# --- Output Models ---

class ClassifyResponse(BaseModel):
    """Output schema for POST /classify"""
    classification: str        # "Hot", "Warm", or "Cold"
    suggested_reply: str


class LeadResponse(BaseModel):
    """Output schema for GET /leads"""
    id: int
    name: str
    email: str
    phone: Optional[str]
    message: str
    source: Optional[str]
    classification: Optional[str]
    suggested_reply: Optional[str]
    contacted: bool
    created_at: str

    @classmethod
    def from_row(cls, row) -> "LeadResponse":
        """Convert a sqlite3.Row object to LeadResponse."""
        return cls(
            id=row["id"],
            name=row["name"],
            email=row["email"],
            phone=row["phone"],
            message=row["message"],
            source=row["source"],
            classification=row["classification"],
            suggested_reply=row["suggested_reply"],
            contacted=bool(row["contacted"]),
            created_at=row["created_at"],
        )


class LeadUpdateContacted(BaseModel):
    """Input schema for PATCH /lead/{id}/contacted"""
    contacted: bool