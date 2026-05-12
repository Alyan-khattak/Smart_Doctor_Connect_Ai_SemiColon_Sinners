import { CheckCircle, XCircle } from "lucide-react";

export default function AvailabilityBadge({ isAvailable }: { isAvailable: boolean }) {
  if (isAvailable) {
    return (
      <span className="inline-flex items-center gap-1.5 bg-green-100 text-green-700 text-xs font-semibold px-3 py-1 rounded-full">
        <CheckCircle className="w-3.5 h-3.5" /> Available Now
      </span>
    );
  }
  return (
    <span className="inline-flex items-center gap-1.5 bg-red-100 text-red-700 text-xs font-semibold px-3 py-1 rounded-full">
      <XCircle className="w-3.5 h-3.5" /> Currently Unavailable
    </span>
  );
}
