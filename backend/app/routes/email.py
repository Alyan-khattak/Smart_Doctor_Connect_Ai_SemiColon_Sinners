from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import AppointmentEmailRequest, LeadEmailRequest
from app.services import email_service, doctor_service

router = APIRouter(prefix="/email", tags=["Email"])


@router.post("/send-appointment")
def send_appointment_email(
    payload: AppointmentEmailRequest,
    db: Session = Depends(get_db),
):
    doctor = doctor_service.get_doctor_by_id(db, payload.doctor_id)
    doctor_email = doctor.email if doctor else ""
    doctor_name = doctor.name if doctor else "Doctor"

    sent = email_service.send_appointment_email(
        doctor_email=doctor_email,
        doctor_name=doctor_name,
        appointment_id=payload.appointment_id,
        patient_name=payload.patient_name,
        patient_contact=payload.patient_contact,
        problem=payload.problem,
        appointment_date=payload.appointment_date,
        appointment_time=payload.appointment_time,
        consultation_type=payload.consultation_type,
    )

    return {"email_sent": sent}


@router.post("/send-lead")
def send_lead_email(
    payload: LeadEmailRequest,
    db: Session = Depends(get_db),
):
    doctor = doctor_service.get_doctor_by_id(db, payload.doctor_id)
    doctor_email = doctor.email if doctor else ""
    doctor_name = doctor.name if doctor else "Doctor"

    sent = email_service.send_lead_email(
        doctor_email=doctor_email,
        doctor_name=doctor_name,
        lead_id=payload.lead_id,
        patient_name=payload.patient_name,
        patient_contact=payload.patient_contact,
        problem=payload.problem,
    )

    return {"email_sent": sent}
