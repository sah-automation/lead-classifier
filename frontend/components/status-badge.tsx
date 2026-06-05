import type { LeadClassification } from "@/types/lead";

type StatusBadgeProps = {
  classification: LeadClassification;
};

const badgeStyles: Record<LeadClassification, string> = {
  Hot: "bg-red-100 text-red-700 border border-red-200",
  Warm: "bg-yellow-100 text-yellow-700 border border-yellow-200",
  Cold: "bg-blue-100 text-blue-700 border border-blue-200",
};

export default function StatusBadge({
  classification,
}: StatusBadgeProps) {
  return (
    <span
      className={`inline-flex rounded-full px-3 py-1 text-sm font-medium ${badgeStyles[classification]}`}
    >
      {classification}
    </span>
  );
}