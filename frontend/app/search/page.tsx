"use client";
import { useEffect, useState, useCallback } from "react";
import { useSearchParams } from "next/navigation";
import { Suspense } from "react";
import { recommendDoctors } from "@/lib/api";
import { RecommendationResponse } from "@/lib/types";
import DoctorCard from "@/components/DoctorCard";
import SafetyNote from "@/components/SafetyNote";
import LoadingState from "@/components/LoadingState";
import ErrorState from "@/components/ErrorState";
import EmptyState from "@/components/EmptyState";
import { CITIES, CONSULTATION_TYPES } from "@/lib/constants";
import { useRouter } from "next/navigation";
import { Brain, Search } from "lucide-react";

function SearchContent() {
  const searchParams = useSearchParams();
  const router = useRouter();

  const [query, setQuery] = useState(searchParams.get("q") || "");
  const [city, setCity] = useState(searchParams.get("city") || "");
  const [consultationType, setConsultationType] = useState(searchParams.get("type") || "");
  const [results, setResults] = useState<RecommendationResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const doSearch = useCallback(async (q: string, c: string, t: string) => {
    if (!q.trim()) return;
    setLoading(true);
    setError("");
    setResults(null);
    try {
      const data = await recommendDoctors({
        query: q,
        city: c,
        consultation_type: t as "online" | "physical" | "both" | "",
      });
      setResults(data);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to fetch recommendations.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    const q = searchParams.get("q") || "";
    const c = searchParams.get("city") || "";
    const t = searchParams.get("type") || "";
    if (q) {
      setQuery(q);
      setCity(c);
      setConsultationType(t);
      doSearch(q, c, t);
    }
  }, [searchParams, doSearch]);

  function handleSearch(e: React.FormEvent) {
    e.preventDefault();
    const params = new URLSearchParams();
    if (query) params.set("q", query);
    if (city) params.set("city", city);
    if (consultationType) params.set("type", consultationType);
    router.push(`/search?${params.toString()}`);
    doSearch(query, city, consultationType);
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Search bar */}
      <form onSubmit={handleSearch} className="bg-white rounded-2xl border border-slate-200 p-4 shadow-sm mb-8">
        <div className="flex flex-col md:flex-row gap-3">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
            <input
              id="search-query"
              type="text"
              placeholder="Symptoms or specialization..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-3 text-sm border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-sky-500 bg-slate-50"
            />
          </div>
          <select
            id="search-city"
            value={city}
            onChange={(e) => setCity(e.target.value)}
            className="py-3 px-4 text-sm border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-sky-500 bg-slate-50 md:w-40"
          >
            <option value="">All Cities</option>
            {CITIES.map((c) => <option key={c} value={c}>{c}</option>)}
          </select>
          <select
            id="search-type"
            value={consultationType}
            onChange={(e) => setConsultationType(e.target.value)}
            className="py-3 px-4 text-sm border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-sky-500 bg-slate-50 md:w-36"
          >
            {CONSULTATION_TYPES.map((t) => <option key={t.value} value={t.value}>{t.label}</option>)}
          </select>
          <button
            id="search-submit"
            type="submit"
            className="bg-sky-500 hover:bg-sky-600 text-white font-semibold px-6 py-3 rounded-xl transition-colors"
          >
            Search
          </button>
        </div>
      </form>

      {/* AI analysis result banner */}
      {results && (
        <div className="bg-gradient-to-r from-violet-50 to-sky-50 border border-violet-200 rounded-2xl p-5 mb-6">
          <div className="flex items-start gap-3">
            <Brain className="w-5 h-5 text-violet-500 shrink-0 mt-0.5" />
            <div>
              <p className="font-semibold text-slate-900">
                AI detected: <span className="text-sky-600">{results.detected_specialization}</span>
                {results.urgency && (
                  <span className={`ml-2 text-xs px-2 py-0.5 rounded-full font-medium ${
                    results.urgency === "high" ? "bg-red-100 text-red-700" :
                    results.urgency === "medium" ? "bg-amber-100 text-amber-700" :
                    "bg-green-100 text-green-700"
                  }`}>
                    {results.urgency} urgency
                  </span>
                )}
              </p>
              {results.ai_reason && (
                <p className="text-sm text-slate-600 mt-1">{results.ai_reason}</p>
              )}
              {results.fallback_used && (
                <p className="text-xs text-slate-400 mt-1">Using keyword analysis (AI unavailable)</p>
              )}
            </div>
          </div>
        </div>
      )}

      {/* States */}
      {loading && <LoadingState message="AI is analyzing your symptoms..." />}
      {error && <ErrorState message={error} />}
      {!loading && !error && results && results.recommended_doctors.length === 0 && (
        <EmptyState message="No doctors found for this query. Try different symptoms or remove city filter." />
      )}

      {/* Doctor grid */}
      {results && results.recommended_doctors.length > 0 && (
        <>
          <p className="text-sm text-slate-500 mb-4">
            Showing {results.recommended_doctors.length} recommended doctor(s)
          </p>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
            {results.recommended_doctors.map((doc) => (
              <DoctorCard
                key={doc.id}
                doctor={doc}
                reason={doc.recommendation_reason}
                score={doc.score}
              />
            ))}
          </div>
        </>
      )}

      {!loading && !query && !results && (
        <EmptyState message="Enter symptoms or a doctor specialization above to get AI-powered recommendations." />
      )}

      <SafetyNote />
    </div>
  );
}

export default function SearchPage() {
  return (
    <Suspense fallback={<LoadingState />}>
      <SearchContent />
    </Suspense>
  );
}
