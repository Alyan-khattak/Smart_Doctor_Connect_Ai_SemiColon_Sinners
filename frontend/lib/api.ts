import {
  Doctor,
  RecommendationRequest,
  RecommendationResponse,
  AvailabilityResponse,
  AppointmentRequest,
  AppointmentSuccessResponse,
  AppointmentConflictResponse,
  ChatbotMessageRequest,
  ChatbotMessageResponse,
  ChatbotLeadRequest,
  ChatbotLeadResponse,
  DashboardResponse,
  TokenResponse,
  DoctorAuthMe,
  DoctorProfileRequest,
} from "./types";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "/api";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(options?.headers || {}),
    },
  });

  const data = await response.json().catch(() => null);

  if (!response.ok) {
    throw new Error(
      (data as { message?: string; detail?: string })?.message ||
        (data as { detail?: string })?.detail ||
        "Something went wrong"
    );
  }

  return data as T;
}

export function getDoctors() {
  return request<Doctor[]>("/doctors");
}

export function getDoctor(id: number) {
  return request<Doctor>(`/doctors/${id}`);
}

export function searchDoctors(params: {
  city?: string;
  specialization?: string;
  consultation_type?: string;
}) {
  const search = new URLSearchParams();
  if (params.city) search.set("city", params.city);
  if (params.specialization) search.set("specialization", params.specialization);
  if (params.consultation_type) search.set("consultation_type", params.consultation_type);
  return request<{ results: Doctor[] }>(`/doctors/search?${search.toString()}`);
}

export function recommendDoctors(payload: RecommendationRequest) {
  return request<RecommendationResponse>("/recommendations", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function getAvailability(doctorId: number, date: string) {
  return request<AvailabilityResponse>(
    `/availability/${doctorId}?date=${encodeURIComponent(date)}`
  );
}

export function bookAppointment(payload: AppointmentRequest) {
  return request<AppointmentSuccessResponse | AppointmentConflictResponse>(
    "/appointments",
    {
      method: "POST",
      body: JSON.stringify(payload),
    }
  );
}

export function sendChatbotMessage(payload: ChatbotMessageRequest) {
  return request<ChatbotMessageResponse>("/chatbot/message", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function saveChatbotLead(payload: ChatbotLeadRequest) {
  return request<ChatbotLeadResponse>("/chatbot/lead", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function getDoctorDashboard(doctorId: number) {
  return request<DashboardResponse>(`/dashboard/doctor/${doctorId}`);
}

// --- Auth APIs ---

export function registerDoctor(payload: any) {
  return request<TokenResponse>("/auth/doctor/register", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function loginDoctor(payload: any) {
  const formBody = new URLSearchParams();
  formBody.append("username", payload.email);
  formBody.append("password", payload.password);

  return request<TokenResponse>("/auth/doctor/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: formBody.toString(),
  });
}

export function getDoctorMe(token: string) {
  return request<DoctorAuthMe>("/auth/doctor/me", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
}

export function createMyDoctorProfile(token: string, payload: DoctorProfileRequest) {
  return request<Doctor>("/doctors/me/profile", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(payload),
  });
}

export function updateMyDoctorProfile(token: string, payload: DoctorProfileRequest) {
  return request<Doctor>("/doctors/me/profile", {
    method: "PUT",
    headers: {
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(payload),
  });
}

export function getDoctorMyDashboard(token: string) {
  return request<DashboardResponse>("/dashboard/me", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
}


