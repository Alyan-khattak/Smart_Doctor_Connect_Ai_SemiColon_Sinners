import { SearchX } from "lucide-react";

export default function EmptyState({ message = "No results found." }: { message?: string }) {
  return (
    <div className="flex flex-col items-center justify-center py-20 gap-4">
      <SearchX className="w-10 h-10 text-slate-300" />
      <p className="text-slate-500 text-sm text-center max-w-xs">{message}</p>
    </div>
  );
}
