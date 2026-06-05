import type { Lead, LeadClassification } from "@/types/lead";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

export async function getLeads(
  classification?: LeadClassification | "All"
): Promise<Lead[]> {
  const url =
    classification && classification !== "All"
      ? `${API_BASE_URL}/leads?classification=${classification}`
      : `${API_BASE_URL}/leads`;

  const response = await fetch(url, {
    method: "GET",
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error("Failed to fetch leads");
  }

  return response.json();
}

export async function markLeadAsContacted(
  leadId: number,
  contacted: boolean = true
): Promise<Lead> {
  const response = await fetch(`${API_BASE_URL}/lead/${leadId}/contacted`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ contacted }),
  });

  if (!response.ok) {
    throw new Error("Failed to update contacted status");
  }

  return response.json();
}