from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from datetime import datetime


# ─────────────────────────────────────────────────────────────
# Doctor Schemas
# ─────────────────────────────────────────────────────────────

class DoctorCreate(BaseModel):
    name: str
    email: str
    specialization: str
    city: str
    location: Optional[str] = None
    consultation_type: str  # online | physical | both
    experience_years: int = 0
    rating: float = 4.5
    is_available: bool = True
    bio: Optional[str] = None


class DoctorUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    specialization: Optional[str] = None
    city: Optional[str] = None
    location: Optional[str] = None
    consultation_type: Optional[str] = None
    experience_years: Optional[int] = None
    rating: Optional[float] = None
    is_available: Optional[bool] = None
    bio: Optional[str] = None


class DoctorResponse(BaseModel):
    id: int
    name: str
    email: str
    specialization: str
    city: str
    location: Optional[str] = None
    consultation_type: str
    experience_years: int
    rating: float
    is_available: bool
    bio: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# ─────────────────────────────────────────────────────────────
# Recommendation Schemas
# ─────────────────────────────────────────────────────────────

class RecommendationRequest(BaseModel):
    query: str
    city: Optional[str] = None
    consultation_type: Optional[str] = None


class RecommendationDoctorResponse(BaseModel):
    id: int
    name: str
    specialization: str
    city: str
    location: Optional[str] = None
    consultation_type: str
    experience_years: int
    rating: float
    is_available: bool
    score: float
    recommendation_reason: str


class RecommendationResponse(BaseModel):
    detected_specialization: str
    urgency: Optional[str] = "medium"
    ai_reason: Optional[str] = None
    recommended_doctors: List[RecommendationDoctorResponse]
    safety_note: str = (
        "This system helps find doctors. It does not provide diagnosis or emergency medical care."
    )
    ai_used: Optional[bool] = None
    fallback_used: Optional[bool] = None


# ─────────────────────────────────────────────────────────────
# Availability Schemas
# ─────────────────────────────────────────────────────────────

class AvailabilityCreate(BaseModel):
    slot_date: str
    slot_time: str


class AvailabilityUpdate(BaseModel):
    is_booked: bool


class AvailabilitySlotResponse(BaseModel):
    slot_id: int
    time: str
    is_booked: bool

    model_config = ConfigDict(from_attributes=True)


class AvailabilityResponse(BaseModel):
    doctor_id: int
    date: str
    slots: List[AvailabilitySlotResponse]
    earliest_available_slot: Optional[str] = None


# ─────────────────────────────────────────────────────────────
# Appointment Schemas
# ─────────────────────────────────────────────────────────────

class AppointmentCreate(BaseModel):
    doctor_id: int
    patient_name: str
    patient_contact: str
    problem: str
    appointment_date: str
    appointment_time: str
    consultation_type: str  # online | physical


class AppointmentStatusUpdate(BaseModel):
    status: str  # pending | confirmed | cancelled | completed


class AppointmentResponse(BaseModel):
    id: int
    doctor_id: int
    patient_name: str
    patient_contact: str
    problem: str
    appointment_date: str
    appointment_time: str
    consultation_type: str
    status: str

    model_config = ConfigDict(from_attributes=True)


# ─────────────────────────────────────────────────────────────
# Chatbot Schemas
# ─────────────────────────────────────────────────────────────

class ChatbotCollectedData(BaseModel):
    patient_name: Optional[str] = None
    patient_contact: Optional[str] = None
    problem: Optional[str] = None


class ChatbotMessageRequest(BaseModel):
    doctor_id: int
    message: str
    conversation_state: str = "START"
    collected_data: ChatbotCollectedData = ChatbotCollectedData()


class ChatbotMessageResponse(BaseModel):
    reply: str
    next_state: str
    collected_data: ChatbotCollectedData
    is_complete: bool


class ChatbotLeadCreate(BaseModel):
    doctor_id: int
    patient_name: str
    patient_contact: str
    problem: str


class ChatbotLeadResponse(BaseModel):
    id: int
    doctor_id: int
    patient_name: str
    patient_contact: str
    problem: str
    status: str

    model_config = ConfigDict(from_attributes=True)


# ─────────────────────────────────────────────────────────────
# Email Schemas
# ─────────────────────────────────────────────────────────────

class AppointmentEmailRequest(BaseModel):
    appointment_id: int
    doctor_id: int
    patient_name: str
    patient_contact: str
    problem: str
    appointment_date: str
    appointment_time: str
    consultation_type: str


class LeadEmailRequest(BaseModel):
    lead_id: int
    doctor_id: int
    patient_name: str
    patient_contact: str
    problem: str


# ─────────────────────────────────────────────────────────────
# Dashboard Schemas
# ─────────────────────────────────────────────────────────────

class DashboardDoctor(BaseModel):
    id: int
    name: str
    specialization: str
    city: str
    is_available: bool


class DashboardStats(BaseModel):
    total_appointments: int
    pending_appointments: int
    today_appointments: int
    new_chatbot_leads: int


class DashboardResponse(BaseModel):
    doctor: DashboardDoctor
    stats: DashboardStats
    appointments: List[AppointmentResponse]
    chatbot_leads: List[ChatbotLeadResponse]
