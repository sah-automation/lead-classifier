export type LeadClassification = "Hot" | "Warm" | "Cold";

export interface Lead {
  id: number;
  name: string;
  email: string;
  phone: string | null;
  message: string;
  source: string | null;
  classification: LeadClassification;
  suggested_reply: string;
  contacted: boolean;
  created_at: string;
}