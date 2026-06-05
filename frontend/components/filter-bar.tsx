import type { LeadClassification } from "@/types/lead";

type FilterValue = "All" | LeadClassification;

type FilterBarProps = {
  selectedFilter: FilterValue;
  onFilterChange: (value: FilterValue) => void;
};

export default function FilterBar({
  selectedFilter,
  onFilterChange,
}: FilterBarProps) {
  return (
    <div className="mb-6 flex items-center justify-between gap-4">
      <div>
        <h2 className="text-lg font-semibold text-gray-900">Leads</h2>
        <p className="text-sm text-gray-500">
          View and manage incoming leads by classification.
        </p>
      </div>

      <div className="flex items-center gap-2">
        <label
          htmlFor="classification-filter"
          className="text-sm font-medium text-gray-700"
        >
          Filter
        </label>
        <select
          id="classification-filter"
          value={selectedFilter}
          onChange={(e) => onFilterChange(e.target.value as FilterValue)}
          className="rounded-md border border-gray-300 bg-white px-3 py-2 text-sm text-gray-700 shadow-sm outline-none focus:border-gray-500"
        >
          <option value="All">All</option>
          <option value="Hot">Hot</option>
          <option value="Warm">Warm</option>
          <option value="Cold">Cold</option>
        </select>
      </div>
    </div>
  );
}