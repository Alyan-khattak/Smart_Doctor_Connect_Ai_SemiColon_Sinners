from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Float,
    DateTime,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.sql import func
from app.database import Base


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    specialization = Column(String, nullable=False, index=True)
    city = Column(String, nullable=False, index=True)
    location = Column(String, nullable=True)
    consultation_type = Column(String, nullable=False)
    experience_years = Column(Integer, default=0)
    rating = Column(Float, default=4.5)
    is_available = Column(Boolean, default=True, index=True)
    bio = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class AvailabilitySlot(Base):
    __tablename__ = "availability_slots"

    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False, index=True)
    slot_date = Column(String, nullable=False, index=True)
    slot_time = Column(String, nullable=False)
    is_booked = Column(Boolean, default=False, index=True)

    __table_args__ = (
        UniqueConstraint(
            "doctor_id",
            "slot_date",
            "slot_time",
            name="uq_slots_doctor_date_time",
        ),
    )


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False, index=True)
    patient_name = Column(String, nullable=False)
    patient_contact = Column(String, nullable=False)
    problem = Column(String, nullable=False)
    appointment_date = Column(String, nullable=False, index=True)
    appointment_time = Column(String, nullable=False)
    consultation_type = Column(String, nullable=False)
    status = Column(String, default="pending", index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint(
            "doctor_id",
            "appointment_date",
            "appointment_time",
            name="uq_appointments_doctor_date_time",
        ),
    )


class ChatbotLead(Base):
    __tablename__ = "chatbot_leads"

    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False, index=True)
    patient_name = Column(String, nullable=False)
    patient_contact = Column(String, nullable=False)
    problem = Column(String, nullable=False)
    status = Column(String, default="new", index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
