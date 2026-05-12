"use client";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { getDoctor, getAvailability, bookAppointment } from "@/lib/api";
import { Doctor, AvailabilityResponse, AppointmentSuccessResponse, AppointmentConflictResponse } from "@/lib/types";
import LoadingState from "@/components/LoadingState";
import ErrorState from "@/components/ErrorState";
import SafetyNote from "@/components/SafetyNote";
import { Calendar, CheckCircle, AlertTriangle, Clock } from "lucide-react";
import { BOOKING_CONSULTATION_TYPES } from "@/lib/constants";

export default function BookingPage() {
  const params = useParams();
  const doctorId = Number(params.doctorId);

  const [doctor, setDoctor] = useState<Doctor | null>(null);
  const [availability, setAvailability] = useState<AvailabilityResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState<AppointmentSuccessResponse | null>(null);
  const [conflict, setConflict] = useState<AppointmentConflictResponse | null>(null);

  const today = new Date().toISOString().split("T")[0];

  const [form, setForm] = useState({
    patient_name: "",
    patient_contact: "",
    problem: "",
    appointment_date: today,
    appointment_time: "",
    consultation_type: "online" as "online" | "physical",
  });

  useEffect(() => {
    Promise.all([
      getDoctor(doctorId),
      getAvailability(doctorId, today),
    ])
      .then(([doc, avail]) => {
        setDoctor(doc);
        setAvailability(avail);
        if (avail.earliest_available_slot) {
          setForm((f) => ({ ...f, appointment_time: avail.earliest_available_slot! }));
        }
      })
      .catch((err) => setError(err.message || "Failed to load."))
      .finally(() => setLoading(false));
  }, [doctorId, today]);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!form.appointment_time) {
      setError("Please select a time slot.");
      return;
    }
    setSubmitting(true);
    setError("");
    setSuccess(null);
    setConflict(null);
    try {
      const result = await bookAppointment({
        doctor_id: doctorId,
        ...form,
      });
      if ("appointment_id" in result) {
        setSuccess(result as AppointmentSuccessResponse);
      } else {
        setConflict(result as AppointmentConflictResponse);
      }
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Booking failed.");
    } finally {
      setSubmitting(false);
    }
  }

  if (loading) return <LoadingState />;
  if (error && !doctor) return <ErrorState message={error} />;

  return (
    <div className="max-w-2xl mx-auto px-4 py-10">
      {/* Header */}
      <div className="bg-gradient-to-r from-sky-500 to-blue-600 text-white rounded-3xl p-6 mb-6">
        <div className="flex items-center gap-3 mb-1">
          <Calendar className="w-5 h-5" />
          <h1 className="font-bold text-lg">Book Appointment</h1>
        </div>
        {doctor && (
          <p className="text-sky-100 text-sm">
            with {doctor.name} — {doctor.specialization}
          </p>
        )}
      </div>

      {/* Success */}
      {success && (
        <div className="bg-green-50 border border-green-200 rounded-2xl p-6 mb-6 text-center">
          <CheckCircle className="w-10 h-10 text-green-500 mx-auto mb-3" />
          <h2 className="font-bold text-green-800 text-lg mb-1">Appointment Booked!</h2>
          <p className="text-green-700 text-sm mb-2">
            Appointment #{success.appointment_id} — Status: <strong>{success.status}</strong>
          </p>
          <p className="text-xs text-green-600">
            {success.email_sent ? "Doctor notified via email." : "Email notification pending."}
          </p>
        </div>
      )}

      {/* Conflict */}
      {conflict && (
        <div className="bg-amber-50 border border-amber-200 rounded-2xl p-6 mb-6">
          <div className="flex items-center gap-2 mb-3">
            <AlertTriangle className="w-5 h-5 text-amber-500" />
            <h2 className="font-bold text-amber-800">Slot Already Booked</h2>
          </div>
          <p className="text-amber-700 text-sm mb-3">{conflict.message}</p>
          {conflict.available_alternative_slots.length > 0 && (
            <div>
              <p className="text-xs font-semibold text-amber-700 mb-2">Available alternative slots:</p>
              <div className="flex flex-wrap gap-2">
                {conflict.available_alternative_slots.map((t) => (
                  <button
                    key={t}
                    onClick={() => {
                      setForm((f) => ({ ...f, appointment_time: t }));
                      setConflict(null);
                    }}
                    className="bg-amber-100 hover:bg-amber-200 text-amber-800 text-sm px-3 py-1.5 rounded-lg font-medium transition-colors"
                  >
                    {t}
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {!success && (
        <form onSubmit={handleSubmit} className="bg-white rounded-2xl border border-slate-200 p-6 space-y-4">
          <div>
            <label className="block text-sm font-semibold text-slate-700 mb-1" htmlFor="patient-name">Full Name</label>
            <input
              id="patient-name"
              required
              type="text"
              placeholder="Ali Khan"
              value={form.patient_name}
              onChange={(e) => setForm((f) => ({ ...f, patient_name: e.target.value }))}
              className="w-full border border-slate-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-sky-500 bg-slate-50"
            />
          </div>
          <div>
            <label className="block text-sm font-semibold text-slate-700 mb-1" htmlFor="patient-contact">Contact Number</label>
            <input
              id="patient-contact"
              required
              type="text"
              placeholder="03001234567"
              value={form.patient_contact}
              onChange={(e) => setForm((f) => ({ ...f, patient_contact: e.target.value }))}
              className="w-full border border-slate-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-sky-500 bg-slate-50"
            />
          </div>
          <div>
            <label className="block text-sm font-semibold text-slate-700 mb-1" htmlFor="problem">Medical Problem</label>
            <textarea
              id="problem"
              required
              placeholder="Describe your medical concern..."
              value={form.problem}
              onChange={(e) => setForm((f) => ({ ...f, problem: e.target.value }))}
              rows={3}
              className="w-full border border-slate-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-sky-500 bg-slate-50 resize-none"
            />
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-sm font-semibold text-slate-700 mb-1" htmlFor="appointment-date">Date</label>
              <input
                id="appointment-date"
                required
                type="date"
                min={today}
                value={form.appointment_date}
                onChange={(e) => {
                  const d = e.target.value;
                  setForm((f) => ({ ...f, appointment_date: d }));
                  getAvailability(doctorId, d).then(setAvailability).catch(() => {});
                }}
                className="w-full border border-slate-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-sky-500 bg-slate-50"
              />
            </div>
            <div>
              <label className="block text-sm font-semibold text-slate-700 mb-1" htmlFor="consultation-type">Type</label>
              <select
                id="consultation-type"
                value={form.consultation_type}
                onChange={(e) => setForm((f) => ({ ...f, consultation_type: e.target.value as "online" | "physical" }))}
                className="w-full border border-slate-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-sky-500 bg-slate-50"
              >
                {BOOKING_CONSULTATION_TYPES.map((t) => (
                  <option key={t.value} value={t.value}>{t.label}</option>
                ))}
              </select>
            </div>
          </div>

          {/* Time slots */}
          {availability && availability.slots.length > 0 && (
            <div>
              <label className="block text-sm font-semibold text-slate-700 mb-2">
                Select Time Slot
              </label>
              {availability.earliest_available_slot && (
                <p className="text-xs text-sky-600 mb-2 flex items-center gap-1">
                  <Clock className="w-3.5 h-3.5" />
                  Earliest available: {availability.earliest_available_slot}
                </p>
              )}
              <div className="grid grid-cols-4 gap-2">
                {availability.slots.map((slot) => (
                  <button
                    key={slot.slot_id}
                    type="button"
                    disabled={slot.is_booked}
                    onClick={() => setForm((f) => ({ ...f, appointment_time: slot.time }))}
                    className={`text-sm py-2 rounded-xl font-medium transition-all border
                      ${slot.is_booked
                        ? "bg-slate-100 text-slate-400 border-slate-200 cursor-not-allowed line-through"
                        : form.appointment_time === slot.time
                        ? "bg-sky-500 text-white border-sky-500"
                        : "bg-white text-slate-700 border-slate-200 hover:border-sky-300"
                      }`}
                  >
                    {slot.time}
                  </button>
                ))}
              </div>
            </div>
          )}

          {error && <p className="text-red-500 text-sm">{error}</p>}

          <button
            id="book-submit-btn"
            type="submit"
            disabled={submitting}
            className="w-full bg-sky-500 hover:bg-sky-600 disabled:bg-sky-300 text-white font-bold py-4 rounded-xl transition-colors text-base"
          >
            {submitting ? "Booking..." : "Confirm Appointment"}
          </button>
        </form>
      )}

      <div className="mt-6">
        <SafetyNote />
      </div>
    </div>
  );
}
