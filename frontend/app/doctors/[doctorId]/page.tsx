"use client";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { getDoctor } from "@/lib/api";
import { Doctor } from "@/lib/types";
import LoadingState from "@/components/LoadingState";
import ErrorState from "@/components/ErrorState";
import AvailabilityBadge from "@/components/AvailabilityBadge";
import { MapPin, Clock, Star, Video, Building2, Calendar, MessageSquare } from "lucide-react";

export default function DoctorProfilePage() {
  const params = useParams();
  const doctorId = Number(params.doctorId);

  const [doctor, setDoctor] = useState<Doctor | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    getDoctor(doctorId)
      .then(setDoctor)
      .catch((err) => setError(err.message || "Doctor not found."))
      .finally(() => setLoading(false));
  }, [doctorId]);

  if (loading) return <LoadingState />;
  if (error || !doctor) return <ErrorState message={error || "Doctor not found."} />;

  return (
    <div className="max-w-4xl mx-auto px-4 py-10">
      {/* Profile header */}
      <div className="bg-gradient-to-r from-sky-600 to-blue-700 rounded-3xl p-8 text-white mb-6">
        <div className="flex flex-col sm:flex-row sm:items-center gap-6">
          <div className="w-20 h-20 rounded-2xl bg-white/20 flex items-center justify-center text-4xl font-bold text-white">
            {doctor.name.charAt(3).toUpperCase()}
          </div>
          <div className="flex-1">
            <h1 className="text-2xl font-extrabold mb-1">{doctor.name}</h1>
            <p className="text-sky-100 font-medium text-lg mb-3">{doctor.specialization}</p>
            <AvailabilityBadge isAvailable={doctor.is_available} />
          </div>
        </div>
      </div>

      {/* Info cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        {[
          { icon: MapPin, label: "City", value: doctor.city },
          { icon: Clock, label: "Experience", value: `${doctor.experience_years} years` },
          { icon: Star, label: "Rating", value: `${doctor.rating} / 5` },
          {
            icon: doctor.consultation_type === "online" ? Video : Building2,
            label: "Consultation",
            value: doctor.consultation_type,
          },
        ].map((item) => (
          <div key={item.label} className="bg-white rounded-2xl border border-slate-200 p-4 text-center">
            <item.icon className="w-5 h-5 text-sky-500 mx-auto mb-2" />
            <p className="text-xs text-slate-500">{item.label}</p>
            <p className="text-sm font-semibold text-slate-900 capitalize">{item.value}</p>
          </div>
        ))}
      </div>

      {/* Bio */}
      {doctor.bio && (
        <div className="bg-white rounded-2xl border border-slate-200 p-6 mb-6">
          <h2 className="font-bold text-slate-900 mb-2">About</h2>
          <p className="text-slate-600 text-sm leading-relaxed">{doctor.bio}</p>
        </div>
      )}

      {/* Location */}
      {doctor.location && (
        <div className="bg-white rounded-2xl border border-slate-200 p-6 mb-6">
          <h2 className="font-bold text-slate-900 mb-1">Clinic / Location</h2>
          <p className="text-slate-600 text-sm">{doctor.location}, {doctor.city}</p>
        </div>
      )}

      {/* CTA */}
      <div className="flex flex-col sm:flex-row gap-3">
        {doctor.is_available ? (
          <Link
            id="book-appointment-btn"
            href={`/book/${doctor.id}`}
            className="flex-1 flex items-center justify-center gap-2 bg-sky-500 hover:bg-sky-600 text-white font-semibold py-4 rounded-2xl transition-colors text-base"
          >
            <Calendar className="w-5 h-5" /> Book Appointment
          </Link>
        ) : (
          <Link
            id="chat-ai-btn"
            href={`/chat/${doctor.id}`}
            className="flex-1 flex items-center justify-center gap-2 bg-violet-500 hover:bg-violet-600 text-white font-semibold py-4 rounded-2xl transition-colors text-base"
          >
            <MessageSquare className="w-5 h-5" /> Chat with AI Assistant
          </Link>
        )}
        <Link
          href="/search"
          className="flex-1 flex items-center justify-center gap-2 bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold py-4 rounded-2xl transition-colors text-base"
        >
          Back to Search
        </Link>
      </div>
    </div>
  );
}
