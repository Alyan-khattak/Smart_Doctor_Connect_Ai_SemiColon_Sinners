import { AlertTriangle } from "lucide-react";
import { SAFETY_NOTE } from "@/lib/constants";

export default function SafetyNote() {
  return (
    <div className="flex items-start gap-3 bg-amber-50 border border-amber-200 rounded-xl p-4 text-sm text-amber-800">
      <AlertTriangle className="w-5 h-5 shrink-0 mt-0.5 text-amber-500" />
      <p>{SAFETY_NOTE}</p>
    </div>
  );
}
