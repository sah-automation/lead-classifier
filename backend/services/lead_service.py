from typing import List, Optional

from database import get_connection
from models.lead import LeadCreate, LeadResponse


def insert_lead(
    lead: LeadCreate,
    classification: str,
    suggested_reply: str
) -> int:
    """Insert a new lead into the database and return its ID."""
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO leads (
                name,
                email,
                phone,
                message,
                source,
                classification,
                suggested_reply,
                contacted
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                lead.name,
                lead.email,
                lead.phone,
                lead.message,
                lead.source,
                classification,
                suggested_reply,
                0,
            ),
        )
        conn.commit()
        return cursor.lastrowid


def get_all_leads(classification: Optional[str] = None) -> List[LeadResponse]:
    """Fetch all leads, optionally filtered by classification."""
    with get_connection() as conn:
        if classification:
            rows = conn.execute(
                """
                SELECT *
                FROM leads
                WHERE classification = ?
                ORDER BY id DESC
                """,
                (classification,),
            ).fetchall()
        else:
            rows = conn.execute(
                """
                SELECT *
                FROM leads
                ORDER BY id DESC
                """
            ).fetchall()

    return [LeadResponse.from_row(row) for row in rows]


def get_lead_by_id(lead_id: int) -> Optional[LeadResponse]:
    """Fetch a single lead by ID."""
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT *
            FROM leads
            WHERE id = ?
            """,
            (lead_id,),
        ).fetchone()

    if not row:
        return None

    return LeadResponse.from_row(row)


def update_contacted_status(lead_id: int, contacted: bool) -> bool:
    """Update contacted status for a lead. Returns True if a row was updated."""
    with get_connection() as conn:
        cursor = conn.execute(
            """
            UPDATE leads
            SET contacted = ?
            WHERE id = ?
            """,
            (int(contacted), lead_id),
        )
        conn.commit()
        return cursor.rowcount > 0