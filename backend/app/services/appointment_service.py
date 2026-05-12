from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models import Appointment
from app.services import availability_service


def check_conflict(db: Session, doctor_id: int, date: str, time: str) -> bool:
    """Returns True if the slot is already booked."""
    existing = (
        db.query(Appointment)
        .filter(
            Appointment.doctor_id == doctor_id,
            Appointment.appointment_date == date,
            Appointment.appointment_time == time,
        )
        .first()
    )
    return existing is not None


def get_alternative_slots(db: Session, doctor_id: int, date: str, booked_time: str) -> List[str]:
    """Return alternative available times for the same doctor and date."""
    available = availability_service.get_available_slot_times(db, doctor_id, date)
    # Exclude the conflicting time
    return [t for t in available if t != booked_time][:3]


def create_appointment(
    db: Session,
    doctor_id: int,
    patient_name: str,
    patient_contact: str,
    problem: str,
    appointment_date: str,
    appointment_time: str,
    consultation_type: str,
) -> Appointment:
    """
    Create appointment and mark slot as booked.
    Raises IntegrityError if duplicate booking occurs at DB level.
    """
    appt = Appointment(
        doctor_id=doctor_id,
        patient_name=patient_name,
        patient_contact=patient_contact,
        problem=problem,
        appointment_date=appointment_date,
        appointment_time=appointment_time,
        consultation_type=consultation_type,
        status="pending",
    )
    db.add(appt)
    db.commit()
    db.refresh(appt)

    # Mark availability slot as booked (best-effort)
    availability_service.mark_slot_booked(db, doctor_id, appointment_date, appointment_time)

    return appt


def get_doctor_appointments(db: Session, doctor_id: int) -> List[Appointment]:
    return (
        db.query(Appointment)
        .filter(Appointment.doctor_id == doctor_id)
        .order_by(Appointment.appointment_date.desc(), Appointment.appointment_time.desc())
        .all()
    )


def get_appointment_by_id(db: Session, appointment_id: int) -> Optional[Appointment]:
    return db.query(Appointment).filter(Appointment.id == appointment_id).first()


def update_appointment_status(db: Session, appointment_id: int, status: str) -> Optional[Appointment]:
    appt = get_appointment_by_id(db, appointment_id)
    if not appt:
        return None
    appt.status = status
    db.commit()
    db.refresh(appt)
    return appt
