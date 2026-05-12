import { ChatbotLead } from "@/lib/types";
import { STATUS_COLORS } from "@/lib/constants";

export default function LeadTable({ leads }: { leads: ChatbotLead[] }) {
  if (!leads.length) {
    return <p className="text-slate-500 text-sm py-6 text-center">No chatbot leads yet.</p>;
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b border-slate-200 text-slate-500">
            <th className="text-left py-3 px-4 font-semibold">Patient</th>
            <th className="text-left py-3 px-4 font-semibold">Contact</th>
            <th className="text-left py-3 px-4 font-semibold">Problem</th>
            <th className="text-left py-3 px-4 font-semibold">Status</th>
          </tr>
        </thead>
        <tbody>
          {leads.map((lead) => (
            <tr key={lead.id} className="border-b border-slate-100 hover:bg-slate-50">
              <td className="py-3 px-4 font-medium text-slate-900">{lead.patient_name}</td>
              <td className="py-3 px-4 text-slate-600">{lead.patient_contact}</td>
              <td className="py-3 px-4 text-slate-600 max-w-xs truncate">{lead.problem}</td>
              <td className="py-3 px-4">
                <span className={`${STATUS_COLORS[lead.status] || "bg-gray-100"} text-xs font-semibold px-2 py-1 rounded-full capitalize`}>
                  {lead.status}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
