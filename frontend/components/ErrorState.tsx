import { AlertCircle } from "lucide-react";

export default function ErrorState({ message = "Something went wrong." }: { message?: string }) {
  return (
    <div className="flex flex-col items-center justify-center py-20 gap-4">
      <AlertCircle className="w-10 h-10 text-red-400" />
      <p className="text-slate-600 text-sm text-center max-w-xs">{message}</p>
    </div>
  );
}
