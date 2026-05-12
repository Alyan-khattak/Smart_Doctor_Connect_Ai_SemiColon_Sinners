"use client";
import { useEffect, useState } from "react";
import { getDoctorDashboard } from "@/lib/api";
import { DashboardResponse } from "@/lib/types";
import LoadingState from "@/components/LoadingState";
import ErrorState from "@/components/ErrorState";
import DashboardStats from "@/components/DashboardStats";
import AppointmentTable from "@/components/AppointmentTable";
import LeadTable from "@/components/LeadTable";
import { LayoutDashboard, CheckCircle, XCircle } from "lucide-react";

export default function DashboardPage() {
  const [doctorId, setDoctorId] = useState("1");
  const [data, setData] = useState<DashboardResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

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

  useEffect(() => {
    loadDashboard(doctorId);
  }, []);

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

          {/* Doctor ID selector */}
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
        </div>
      )}
    </div>
  );
}
