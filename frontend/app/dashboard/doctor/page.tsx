"use client";
import { useEffect, useState } from "react";
import { getDoctorDashboard, getDoctorMyDashboard } from "@/lib/api";
import { DashboardResponse } from "@/lib/types";
import LoadingState from "@/components/LoadingState";
import ErrorState from "@/components/ErrorState";
import DashboardStats from "@/components/DashboardStats";
import AppointmentTable from "@/components/AppointmentTable";
import LeadTable from "@/components/LeadTable";
import { LayoutDashboard, CheckCircle, XCircle, Bot, Send } from "lucide-react";

export default function DashboardPage() {
  const [doctorId, setDoctorId] = useState("1");
  const [data, setData] = useState<DashboardResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [isAuthMode, setIsAuthMode] = useState(false);
  const [assistantInput, setAssistantInput] = useState("");
  const [assistantMessages, setAssistantMessages] = useState([
    {
      role: "assistant",
      text: "I am the doctor-side assistant. I can summarize your appointments and chatbot leads from this dashboard.",
    },
  ]);

  function loadDashboard(id: string) {
    if (!id) return;
    setLoading(true);
    setError("");
    setData(null);
    getDoctorDashboard(Number(id))
      .then(setData)
      .catch((err) => setError(err.message || "Failed to load dashboard."))
      .finally(() => setLoading(false));
  }

  function loadMyDashboard(token: string) {
    setLoading(true);
    setError("");
    setData(null);
    getDoctorMyDashboard(token)
      .then(setData)
      .catch((err) => setError(err.message || "Failed to load your dashboard."))
      .finally(() => setLoading(false));
  }

  useEffect(() => {
    const token = localStorage.getItem("doctor_token");
    if (token) {
      setIsAuthMode(true);
      loadMyDashboard(token);
    } else {
      setIsAuthMode(false);
      loadDashboard(doctorId);
    }
  }, []);

  function handleDoctorAssistant() {
    const message = assistantInput.trim();
    if (!message || !data) return;

    const lower = message.toLowerCase();
    let reply = "Use the appointments and chatbot lead tables on this dashboard to review patient requests. I do not chat with patients from the doctor account.";

    if (lower.includes("appointment")) {
      reply = `You currently have ${data.stats.total_appointments} appointments, including ${data.stats.pending_appointments} pending and ${data.stats.today_appointments} today.`;
    } else if (lower.includes("lead") || lower.includes("chatbot")) {
      reply = `You currently have ${data.stats.new_chatbot_leads} new chatbot leads. Patient-side chatbot messages collect name, email, and problem before notifying you.`;
    } else if (lower.includes("email") || lower.includes("mail")) {
      reply = "Appointment and chatbot notifications are sent by backend SMTP. Patients must provide an email so confirmations and follow-ups can be delivered.";
    }

    setAssistantMessages((prev) => [
      ...prev,
      { role: "doctor", text: message },
      { role: "assistant", text: reply },
    ]);
    setAssistantInput("");
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="bg-gradient-to-r from-slate-800 to-slate-900 text-white rounded-3xl p-6 mb-6">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-white/10 rounded-xl flex items-center justify-center">
              <LayoutDashboard className="w-5 h-5" />
            </div>
            <div>
              <h1 className="text-xl font-bold">Doctor Dashboard</h1>
              {data?.doctor && (
                <p className="text-slate-300 text-sm">
                  {data.doctor.name} — {data.doctor.specialization}
                  <span className={`ml-2 inline-flex items-center gap-1 text-xs px-2 py-0.5 rounded-full ${data.doctor.is_available ? "bg-green-500/20 text-green-300" : "bg-red-500/20 text-red-300"}`}>
                    {data.doctor.is_available ? <CheckCircle className="w-3 h-3" /> : <XCircle className="w-3 h-3" />}
                    {data.doctor.is_available ? "Available" : "Unavailable"}
                  </span>
                </p>
              )}
            </div>
          </div>

          {/* Doctor ID selector (only if not authenticated) */}
          {!isAuthMode && (
            <div className="flex gap-2">
              <input
                id="doctor-id-input"
                type="number"
                min="1"
                value={doctorId}
                onChange={(e) => setDoctorId(e.target.value)}
                placeholder="Doctor ID"
                className="w-28 bg-white/10 text-white placeholder-slate-400 border border-white/20 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-white/30"
              />
              <button
                id="load-dashboard-btn"
                onClick={() => loadDashboard(doctorId)}
                className="bg-sky-500 hover:bg-sky-600 text-white text-sm font-semibold px-4 py-2 rounded-xl transition-colors"
              >
                Load
              </button>
            </div>
          )}
        </div>
      </div>

      {loading && <LoadingState />}
      {error && <ErrorState message={error} />}

      {data && (
        <div className="space-y-6">
          {/* Stats */}
          <DashboardStats stats={data.stats} />

          {/* Appointments */}
          <div className="bg-white rounded-2xl border border-slate-200 overflow-hidden">
            <div className="px-6 py-4 border-b border-slate-200">
              <h2 className="font-bold text-slate-900">Appointments</h2>
              <p className="text-xs text-slate-500">{data.appointments.length} total</p>
            </div>
            <AppointmentTable appointments={data.appointments} />
          </div>

          {/* Chatbot leads */}
          <div className="bg-white rounded-2xl border border-slate-200 overflow-hidden">
            <div className="px-6 py-4 border-b border-slate-200">
              <h2 className="font-bold text-slate-900">Chatbot Leads</h2>
              <p className="text-xs text-slate-500">{data.chatbot_leads.length} total</p>
            </div>
            <LeadTable leads={data.chatbot_leads} />
          </div>

          {/* Doctor-side assistant */}
          <div className="bg-white rounded-2xl border border-slate-200 overflow-hidden">
            <div className="px-6 py-4 border-b border-slate-200 flex items-center gap-2">
              <Bot className="w-5 h-5 text-sky-600" />
              <div>
                <h2 className="font-bold text-slate-900">Doctor Assistant</h2>
                <p className="text-xs text-slate-500">For dashboard summaries and follow-up guidance.</p>
              </div>
            </div>
            <div className="p-4 space-y-3 max-h-72 overflow-y-auto">
              {assistantMessages.map((msg, index) => (
                <div
                  key={`${msg.role}-${index}`}
                  className={`flex ${msg.role === "doctor" ? "justify-end" : "justify-start"}`}
                >
                  <div
                    className={`max-w-xl rounded-2xl px-4 py-2.5 text-sm ${
                      msg.role === "doctor"
                        ? "bg-sky-500 text-white"
                        : "bg-slate-100 text-slate-800"
                    }`}
                  >
                    {msg.text}
                  </div>
                </div>
              ))}
            </div>
            <div className="border-t border-slate-200 p-4 flex gap-3">
              <input
                value={assistantInput}
                onChange={(event) => setAssistantInput(event.target.value)}
                onKeyDown={(event) => event.key === "Enter" && handleDoctorAssistant()}
                placeholder="Ask about appointments, leads, or emails..."
                className="flex-1 border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-sky-500 bg-slate-50"
              />
              <button
                onClick={handleDoctorAssistant}
                disabled={!assistantInput.trim()}
                className="w-10 h-10 bg-sky-500 hover:bg-sky-600 disabled:bg-sky-300 text-white rounded-xl flex items-center justify-center transition-colors"
                aria-label="Send doctor assistant message"
              >
                <Send className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
