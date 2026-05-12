import { Loader2 } from "lucide-react";

export default function LoadingState({ message = "Loading..." }: { message?: string }) {
  return (
    <div className="flex flex-col items-center justify-center py-20 gap-4">
      <Loader2 className="w-10 h-10 text-sky-500 animate-spin" />
      <p className="text-slate-500 text-sm">{message}</p>
    </div>
  );
}
