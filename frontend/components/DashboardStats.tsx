import { DashboardStats as Stats } from "@/lib/types";
import { Calendar, Clock, Users, MessageSquare } from "lucide-react";

export default function DashboardStats({ stats }: { stats: Stats }) {
  const cards = [
    {
      label: "Total Appointments",
      value: stats.total_appointments,
      icon: Calendar,
      color: "bg-sky-500",
    },
    {
      label: "Pending",
      value: stats.pending_appointments,
      icon: Clock,
      color: "bg-amber-500",
    },
    {
      label: "Today",
      value: stats.today_appointments,
      icon: Users,
      color: "bg-green-500",
    },
    {
      label: "New Leads",
      value: stats.new_chatbot_leads,
      icon: MessageSquare,
      color: "bg-violet-500",
    },
  ];

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      {cards.map((card) => (
        <div key={card.label} className="bg-white rounded-2xl border border-slate-200 p-5">
          <div className="flex items-center justify-between mb-3">
            <p className="text-sm text-slate-500">{card.label}</p>
            <div className={`${card.color} w-8 h-8 rounded-lg flex items-center justify-center`}>
              <card.icon className="w-4 h-4 text-white" />
            </div>
          </div>
          <p className="text-3xl font-bold text-slate-900">{card.value}</p>
        </div>
      ))}
    </div>
  );
}
