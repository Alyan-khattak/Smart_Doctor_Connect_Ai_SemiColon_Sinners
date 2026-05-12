import Link from "next/link";
import { MapPin, Clock, Star, Video, Building2, CheckCircle, XCircle } from "lucide-react";
import { RecommendationDoctor, Doctor } from "@/lib/types";

type Props = {
  doctor: RecommendationDoctor | Doctor;
  reason?: string;
  score?: number;
};

export default function DoctorCard({ doctor, reason, score }: Props) {
  const isAvailable = doctor.is_available;

  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-sm hover:shadow-md transition-all duration-200 overflow-hidden">
      {/* Header */}
      <div className="bg-gradient-to-r from-sky-500 to-blue-600 p-5">
        <div className="flex items-start justify-between gap-3">
          <div>
            <h3 className="text-white font-bold text-lg">{doctor.name}</h3>
            <p className="text-sky-100 text-sm font-medium">{doctor.specialization}</p>
          </div>
          <div className="shrink-0">
            {isAvailable ? (
              <span className="flex items-center gap-1 bg-green-400/20 text-green-100 text-xs font-semibold px-2 py-1 rounded-full border border-green-400/30">
                <CheckCircle className="w-3 h-3" /> Available
              </span>
            ) : (
              <span className="flex items-center gap-1 bg-red-400/20 text-red-100 text-xs font-semibold px-2 py-1 rounded-full border border-red-400/30">
                <XCircle className="w-3 h-3" /> Unavailable
              </span>
            )}
          </div>
        </div>
      </div>

      {/* Body */}
      <div className="p-5 space-y-3">
        <div className="flex flex-wrap gap-3 text-sm text-slate-600">
          <span className="flex items-center gap-1">
            <MapPin className="w-4 h-4 text-slate-400" />
            {doctor.city}
            {doctor.location ? ` — ${doctor.location}` : ""}
          </span>
          <span className="flex items-center gap-1">
            {doctor.consultation_type === "online" ? (
              <Video className="w-4 h-4 text-sky-500" />
            ) : (
              <Building2 className="w-4 h-4 text-slate-400" />
            )}
            <span className="capitalize">{doctor.consultation_type}</span>
          </span>
          <span className="flex items-center gap-1">
            <Clock className="w-4 h-4 text-slate-400" />
            {doctor.experience_years} yrs exp
          </span>
          <span className="flex items-center gap-1">
            <Star className="w-4 h-4 text-amber-400 fill-amber-400" />
            {doctor.rating}
          </span>
        </div>

        {reason && (
          <p className="text-xs text-slate-500 bg-slate-50 rounded-lg px-3 py-2 leading-relaxed">
            {reason}
          </p>
        )}

        {score !== undefined && (
          <div className="flex items-center gap-2">
            <div className="flex-1 h-1.5 bg-slate-100 rounded-full overflow-hidden">
              <div
                className="h-full bg-sky-500 rounded-full"
                style={{ width: `${Math.min((score / 130) * 100, 100)}%` }}
              />
            </div>
            <span className="text-xs text-slate-500 shrink-0">Score: {score}</span>
          </div>
        )}

        <div className="flex gap-2 pt-1">
          <Link
            href={`/doctors/${doctor.id}`}
            className="flex-1 text-center bg-slate-100 hover:bg-slate-200 text-slate-700 text-sm font-semibold py-2 rounded-lg transition-colors"
          >
            View Profile
          </Link>
          {isAvailable ? (
            <Link
              href={`/book/${doctor.id}`}
              className="flex-1 text-center bg-sky-500 hover:bg-sky-600 text-white text-sm font-semibold py-2 rounded-lg transition-colors"
            >
              Book Now
            </Link>
          ) : (
            <Link
              href={`/chat/${doctor.id}`}
              className="flex-1 text-center bg-violet-500 hover:bg-violet-600 text-white text-sm font-semibold py-2 rounded-lg transition-colors"
            >
              Chat AI
            </Link>
          )}
        </div>
      </div>
    </div>
  );
}
