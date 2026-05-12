"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { Search, Stethoscope, Brain, Calendar, MessageSquare, Star, MapPin } from "lucide-react";
import SafetyNote from "@/components/SafetyNote";
import { CITIES, CONSULTATION_TYPES } from "@/lib/constants";

export default function HomePage() {
  const router = useRouter();
  const [query, setQuery] = useState("");
  const [city, setCity] = useState("");
  const [consultationType, setConsultationType] = useState("");

  function handleSearch(e: React.FormEvent) {
    e.preventDefault();
    const params = new URLSearchParams();
    if (query) params.set("q", query);
    if (city) params.set("city", city);
    if (consultationType) params.set("type", consultationType);
    router.push(`/search?${params.toString()}`);
  }

  return (
    <div>
      {/* Hero */}
      <section className="bg-gradient-to-br from-sky-600 via-blue-600 to-indigo-700 text-white py-20 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 bg-white/20 text-white text-xs font-semibold px-4 py-1.5 rounded-full mb-6 backdrop-blur-sm">
            <Brain className="w-3.5 h-3.5" /> AI-Powered Doctor Discovery
          </div>
          <h1 className="text-4xl md:text-5xl font-extrabold leading-tight mb-4">
            Find the Right Doctor<br />in Pakistan Instantly
          </h1>
          <p className="text-sky-100 text-lg mb-10 max-w-2xl mx-auto">
            Describe your symptoms. Our AI detects the right specialization and recommends the best available doctors in your city.
          </p>

          {/* Search form */}
          <form
            onSubmit={handleSearch}
            className="bg-white rounded-2xl p-4 shadow-2xl max-w-3xl mx-auto"
          >
            <div className="flex flex-col md:flex-row gap-3">
              <div className="flex-1 relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                <input
                  id="symptom-input"
                  type="text"
                  placeholder="Describe symptoms or specialization (e.g. back pain, Cardiologist)"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  className="w-full pl-10 pr-4 py-3 text-slate-800 text-sm bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-sky-500"
                />
              </div>
              <select
                id="city-select"
                value={city}
                onChange={(e) => setCity(e.target.value)}
                className="py-3 px-4 text-slate-700 text-sm bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-sky-500 md:w-40"
              >
                <option value="">All Cities</option>
                {CITIES.map((c) => (
                  <option key={c} value={c}>{c}</option>
                ))}
              </select>
              <select
                id="type-select"
                value={consultationType}
                onChange={(e) => setConsultationType(e.target.value)}
                className="py-3 px-4 text-slate-700 text-sm bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-sky-500 md:w-36"
              >
                {CONSULTATION_TYPES.map((t) => (
                  <option key={t.value} value={t.value}>{t.label}</option>
                ))}
              </select>
              <button
                id="search-btn"
                type="submit"
                className="bg-sky-500 hover:bg-sky-600 text-white font-semibold px-6 py-3 rounded-xl transition-colors whitespace-nowrap"
              >
                Search AI
              </button>
            </div>
          </form>
        </div>
      </section>

      {/* Features */}
      <section className="py-16 px-4 max-w-7xl mx-auto">
        <h2 className="text-2xl font-bold text-slate-900 text-center mb-10">How It Works</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {[
            {
              icon: Search,
              color: "bg-sky-100 text-sky-600",
              title: "Describe Symptoms",
              desc: "Type your symptoms or the specialist you need.",
            },
            {
              icon: Brain,
              color: "bg-violet-100 text-violet-600",
              title: "AI Analysis",
              desc: "Groq AI detects the right specialization and urgency.",
            },
            {
              icon: Star,
              color: "bg-amber-100 text-amber-600",
              title: "Smart Ranking",
              desc: "Doctors ranked by match, availability, rating, and experience.",
            },
            {
              icon: Calendar,
              color: "bg-green-100 text-green-600",
              title: "Instant Booking",
              desc: "Book appointments without double booking conflicts.",
            },
          ].map((f) => (
            <div key={f.title} className="bg-white rounded-2xl border border-slate-200 p-6 text-center">
              <div className={`${f.color} w-12 h-12 rounded-2xl flex items-center justify-center mx-auto mb-4`}>
                <f.icon className="w-6 h-6" />
              </div>
              <h3 className="font-bold text-slate-900 mb-2">{f.title}</h3>
              <p className="text-slate-500 text-sm">{f.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Quick searches */}
      <section className="py-10 px-4 bg-white border-t border-slate-200">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-lg font-bold text-slate-700 mb-4 text-center">Quick Searches</h2>
          <div className="flex flex-wrap justify-center gap-3">
            {[
              "I have back pain",
              "skin allergy",
              "chest pain",
              "child fever",
              "headache",
              "diabetes",
              "eye pain",
              "stomach pain",
            ].map((q) => (
              <button
                key={q}
                onClick={() => {
                  setQuery(q);
                  router.push(`/search?q=${encodeURIComponent(q)}`);
                }}
                className="bg-slate-100 hover:bg-sky-50 hover:text-sky-700 hover:border-sky-200 border border-slate-200 text-slate-700 text-sm px-4 py-2 rounded-full transition-all"
              >
                {q}
              </button>
            ))}
          </div>
        </div>
      </section>

      {/* Safety note */}
      <section className="py-8 px-4 max-w-3xl mx-auto">
        <SafetyNote />
      </section>
    </div>
  );
}
