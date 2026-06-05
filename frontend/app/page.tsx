"use client";

import { useEffect, useState } from "react";
import FilterBar from "@/components/filter-bar";
import LeadsTable from "@/components/leads-table";
import { getLeads, markLeadAsContacted } from "@/lib/api";
import type { Lead, LeadClassification } from "@/types/lead";

type FilterValue = "All" | LeadClassification;

export default function HomePage() {
  const [leads, setLeads] = useState<Lead[]>([]);
  const [selectedFilter, setSelectedFilter] = useState<FilterValue>("All");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [updatingLeadId, setUpdatingLeadId] = useState<number | null>(null);

  async function loadLeads(filter: FilterValue) {
    try {
      setLoading(true);
      setError(null);
      const data = await getLeads(filter);
      setLeads(data);
    } catch (err) {
      setError("Failed to load leads. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadLeads(selectedFilter);
  }, [selectedFilter]);

  async function handleMarkAsContacted(leadId: number) {
    try {
      setUpdatingLeadId(leadId);
      const updatedLead = await markLeadAsContacted(leadId, true);

      setLeads((prevLeads) =>
        prevLeads.map((lead) =>
          lead.id === leadId ? updatedLead : lead
        )
      );
    } catch (err) {
      setError("Failed to update lead status.");
    } finally {
      setUpdatingLeadId(null);
    }
  }

  return (
    <main className="min-h-screen bg-gray-50 px-6 py-10">
      <div className="mx-auto max-w-7xl">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">
            Lead Management Dashboard
          </h1>
          <p className="mt-2 text-sm text-gray-600">
            View, filter, and manage inbound leads from your backend.
          </p>
        </div>

        <FilterBar
          selectedFilter={selectedFilter}
          onFilterChange={setSelectedFilter}
        />

        {loading ? (
          <div className="rounded-lg border border-gray-200 bg-white p-8 text-center text-sm text-gray-500 shadow-sm">
            Loading leads...
          </div>
        ) : error ? (
          <div className="rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-700">
            {error}
          </div>
        ) : (
          <LeadsTable
            leads={leads}
            updatingLeadId={updatingLeadId}
            onMarkAsContacted={handleMarkAsContacted}
          />
        )}
      </div>
    </main>
  );
}