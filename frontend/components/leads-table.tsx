import type { Lead } from "@/types/lead";
import StatusBadge from "./status-badge";

type LeadsTableProps = {
  leads: Lead[];
  updatingLeadId: number | null;
  onMarkAsContacted: (leadId: number) => void;
};

function truncateMessage(message: string, maxLength: number = 80) {
  if (message.length <= maxLength) return message;
  return `${message.slice(0, maxLength)}...`;
}

export default function LeadsTable({
  leads,
  updatingLeadId,
  onMarkAsContacted,
}: LeadsTableProps) {
  if (leads.length === 0) {
    return (
      <div className="rounded-lg border border-dashed border-gray-300 bg-white p-8 text-center text-sm text-gray-500">
        No leads found for the selected filter.
      </div>
    );
  }

  return (
    <div className="overflow-x-auto rounded-xl border border-gray-200 bg-white shadow-sm">
      <table className="min-w-full text-left text-sm text-gray-700">
        <thead className="bg-gray-50 text-xs uppercase tracking-wide text-gray-500">
          <tr>
            <th className="px-4 py-3 font-semibold">Name</th>
            <th className="px-4 py-3 font-semibold">Email</th>
            <th className="px-4 py-3 font-semibold">Phone</th>
            <th className="px-4 py-3 font-semibold">Source</th>
            <th className="px-4 py-3 font-semibold">Message</th>
            <th className="px-4 py-3 font-semibold">Classification</th>
            <th className="px-4 py-3 font-semibold">Suggested Reply</th>
            <th className="px-4 py-3 font-semibold">Status</th>
            <th className="px-4 py-3 font-semibold">Action</th>
          </tr>
        </thead>

        <tbody className="divide-y divide-gray-200">
          {leads.map((lead) => (
            <tr key={lead.id} className="align-top">
              <td className="px-4 py-4 font-medium text-gray-900">{lead.name}</td>
              <td className="px-4 py-4">{lead.email}</td>
              <td className="px-4 py-4">{lead.phone || "-"}</td>
              <td className="px-4 py-4 capitalize">{lead.source || "-"}</td>
              <td className="max-w-xs px-4 py-4 text-gray-600" title={lead.message}>
                {truncateMessage(lead.message)}
              </td>
              <td className="px-4 py-4">
                <StatusBadge classification={lead.classification} />
              </td>
              <td className="max-w-sm px-4 py-4 text-gray-600">
                {lead.suggested_reply}
              </td>
              <td className="px-4 py-4">
                {lead.contacted ? (
                  <span className="inline-flex rounded-full bg-green-100 px-3 py-1 text-xs font-medium text-green-700">
                    Contacted
                  </span>
                ) : (
                  <span className="inline-flex rounded-full bg-gray-100 px-3 py-1 text-xs font-medium text-gray-600">
                    Pending
                  </span>
                )}
              </td>
              <td className="px-4 py-4">
                <button
                  type="button"
                  onClick={() => onMarkAsContacted(lead.id)}
                  disabled={lead.contacted || updatingLeadId === lead.id}
                  className="rounded-md bg-gray-900 px-3 py-2 text-sm font-medium text-white transition hover:bg-gray-700 disabled:cursor-not-allowed disabled:bg-gray-300"
                >
                  {lead.contacted
                    ? "Already Contacted"
                    : updatingLeadId === lead.id
                    ? "Updating..."
                    : "Mark as Contacted"}
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}