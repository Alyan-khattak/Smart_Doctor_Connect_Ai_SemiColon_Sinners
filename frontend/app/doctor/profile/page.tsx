"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { getDoctorMe, createMyDoctorProfile, updateMyDoctorProfile } from "@/lib/api";
import { DoctorProfileRequest, DoctorAuthMe } from "@/lib/types";

export default function ProfilePage() {
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [authData, setAuthData] = useState<DoctorAuthMe | null>(null);
  
  const [formData, setFormData] = useState<DoctorProfileRequest>({
    specialization: "",
    city: "",
    location: "",
    consultation_type: "both",
    experience_years: 0,
    bio: "",
  });

  useEffect(() => {
    const token = localStorage.getItem("doctor_token");
    if (!token) {
      router.push("/doctor/login");
      return;
    }

    getDoctorMe(token)
      .then(async (data) => {
        setAuthData(data);
        if (data.has_profile) {
          // If profile exists, fetch it using the standard GET /doctors/{id} since it's public
          const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/doctors/${data.profile_id}`);
          if (res.ok) {
            const profile = await res.json();
            setFormData({
              specialization: profile.specialization,
              city: profile.city,
              location: profile.location || "",
              consultation_type: profile.consultation_type,
              experience_years: profile.experience_years,
              bio: profile.bio || "",
            });
          }
        }
      })
      .catch((err) => {
        console.error("Auth error:", err);
        localStorage.removeItem("doctor_token");
        router.push("/doctor/login");
      })
      .finally(() => {
        setLoading(false);
      });
  }, [router]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    setSaving(true);
    
    const token = localStorage.getItem("doctor_token");
    if (!token) {
      router.push("/doctor/login");
      return;
    }

    try {
      if (authData?.has_profile) {
        await updateMyDoctorProfile(token, formData);
        setSuccess("Profile updated successfully!");
        const updatedAuthData = await getDoctorMe(token);
        setAuthData(updatedAuthData);
        router.push("/dashboard/doctor");
      } else {
        await createMyDoctorProfile(token, formData);
        setSuccess("Profile created successfully!");
        const updatedAuthData = await getDoctorMe(token);
        setAuthData(updatedAuthData);
        router.push("/dashboard/doctor");
      }
    } catch (err: any) {
      setError(err.message || "Failed to save profile.");
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return <div className="min-h-screen flex items-center justify-center">Loading...</div>;
  }

  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-slate-900 mb-2">Doctor Profile</h1>
      <p className="text-slate-600 mb-8">
        {authData?.has_profile ? "Update your public profile details." : "Complete your profile to appear in search results."}
      </p>

      {error && <div className="bg-red-50 text-red-600 p-4 rounded-lg mb-6">{error}</div>}
      {success && <div className="bg-green-50 text-green-600 p-4 rounded-lg mb-6">{success}</div>}

      <form onSubmit={handleSubmit} className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Specialization</label>
            <input
              type="text"
              required
              placeholder="e.g. Cardiologist"
              className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-sky-500 focus:border-sky-500"
              value={formData.specialization}
              onChange={(e) => setFormData({ ...formData, specialization: e.target.value })}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">City</label>
            <input
              type="text"
              required
              placeholder="e.g. Lahore"
              className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-sky-500 focus:border-sky-500"
              value={formData.city}
              onChange={(e) => setFormData({ ...formData, city: e.target.value })}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Clinic/Hospital Location</label>
            <input
              type="text"
              placeholder="e.g. Johar Town Clinic"
              className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-sky-500 focus:border-sky-500"
              value={formData.location || ""}
              onChange={(e) => setFormData({ ...formData, location: e.target.value })}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Consultation Type</label>
            <select
              className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-sky-500 focus:border-sky-500"
              value={formData.consultation_type}
              onChange={(e) => setFormData({ ...formData, consultation_type: e.target.value as any })}
            >
              <option value="both">Both</option>
              <option value="online">Online</option>
              <option value="physical">Physical</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Experience (Years)</label>
            <input
              type="number"
              min="0"
              required
              className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-sky-500 focus:border-sky-500"
              value={formData.experience_years}
              onChange={(e) => setFormData({ ...formData, experience_years: parseInt(e.target.value) || 0 })}
            />
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Bio</label>
          <textarea
            rows={4}
            className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-sky-500 focus:border-sky-500"
            placeholder="Tell patients about your expertise..."
            value={formData.bio || ""}
            onChange={(e) => setFormData({ ...formData, bio: e.target.value })}
          />
        </div>

        <div className="flex justify-end pt-4">
          <button
            type="submit"
            disabled={saving}
            className="bg-sky-500 hover:bg-sky-600 text-white font-medium py-2 px-6 rounded-lg transition-colors disabled:opacity-50"
          >
            {saving ? "Saving..." : "Save Profile"}
          </button>
        </div>
      </form>
    </div>
  );
}
