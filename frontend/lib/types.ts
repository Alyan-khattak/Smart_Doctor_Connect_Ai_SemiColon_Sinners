// TypeScript types matching backend API contracts exactly (snake_case as per AGENTS.md)

export type TokenResponse = {
  access_token: string;
  token_type: string;
};

export type DoctorAuthMe = {
  auth: {
    id: number;
    email: string;
    full_name: string;
  };
  has_profile: boolean;
  profile_id: number | null;
};

export type DoctorProfileRequest = {
  specialization: string;
  city: string;
  location?: string | null;
  consultation_type: "online" | "physical" | "both";
  experience_years: number;
  bio?: string | null;
};

export type Doctor = {
  id: number;
  name: string;
  email?: string;
  specialization: string;
  city: string;
  location?: string | null;
  consultation_type: "online" | "physical" | "both";
  experience_years: number;
  rating: number;
  is_available: boolean;
  bio?: string | null;
};

export type RecommendationRequest = {
  query: string;
  city: string;
  consultation_type?: "online" | "physical" | "both" | "";
};

export type RecommendationDoctor = {
  id: number;
  name: string;
  specialization: string;
  city: string;
  location?: string | null;
  consultation_type: "online" | "physical" | "both";
  experience_years: number;
  rating: number;
  is_available: boolean;
  score: number;
  recommendation_reason: string;
};

export type RecommendationResponse = {
  detected_specialization: string;
  urgency?: "low" | "medium" | "high" | string;
  ai_reason?: string;
  recommended_doctors: RecommendationDoctor[];
  safety_note: string;
  ai_used?: boolean;
  fallback_used?: boolean;
};

export type AvailabilitySlot = {
  slot_id: number;
  time: string;
  is_booked: boolean;
};

export type AvailabilityResponse = {
  doctor_id: number;
  date: string;
  slots: AvailabilitySlot[];
  earliest_available_slot?: string | null;
};

export type AppointmentRequest = {
  doctor_id: number;
  patient_name: string;
  patient_contact: string;
  problem: string;
  appointment_date: string;
  appointment_time: string;
  consultation_type: "online" | "physical";
};

export type AppointmentSuccessResponse = {
  message: string;
  appointment_id: number;
  status: "pending" | "confirmed" | "cancelled" | "completed";
  email_sent: boolean;
};

export type AppointmentConflictResponse = {
  message: string;
  available_alternative_slots: string[];
};

export type Appointment = {
  id: number;
  doctor_id: number;
  patient_name: string;
  patient_contact: string;
  problem: string;
  appointment_date: string;
  appointment_time: string;
  consultation_type: "online" | "physical";
  status: "pending" | "confirmed" | "cancelled" | "completed";
};

export type ChatbotState =
  | "START"
  | "ASK_NAME"
  | "ASK_CONTACT"
  | "ASK_PROBLEM"
  | "CONFIRM_DETAILS"
  | "SAVE_LEAD"
  | "SEND_EMAIL"
  | "END";

export type ChatbotCollectedData = {
  patient_name: string | null;
  patient_contact: string | null;
  problem: string | null;
};

export type ChatbotMessageRequest = {
  doctor_id: number;
  message: string;
  conversation_state: ChatbotState;
  collected_data: ChatbotCollectedData;
};

export type ChatbotMessageResponse = {
  reply: string;
  next_state: ChatbotState;
  collected_data: ChatbotCollectedData;
  is_complete: boolean;
};

export type ChatbotLeadRequest = {
  doctor_id: number;
  patient_name: string;
  patient_contact: string;
  problem: string;
};

export type ChatbotLeadResponse = {
  message: string;
  lead_id: number;
  email_sent: boolean;
};

export type ChatMessage = {
  id: string;
  sender: "patient" | "ai" | "system";
  text: string;
};

export type DashboardDoctor = {
  id: number;
  name: string;
  specialization: string;
  city: string;
  is_available: boolean;
};

export type DashboardStats = {
  total_appointments: number;
  pending_appointments: number;
  today_appointments: number;
  new_chatbot_leads: number;
};

export type ChatbotLead = {
  id: number;
  patient_name: string;
  patient_contact: string;
  problem: string;
  status: "new" | "contacted" | "closed";
  created_at?: string;
};

export type DashboardResponse = {
  doctor: DashboardDoctor;
  stats: DashboardStats;
  appointments: Appointment[];
  chatbot_leads: ChatbotLead[];
};
