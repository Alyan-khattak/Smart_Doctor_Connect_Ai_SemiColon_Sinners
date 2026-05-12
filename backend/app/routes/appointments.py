from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import AppointmentCreate, AppointmentStatusUpdate, AppointmentResponse
from app.services import appointment_service, doctor_service, email_service

router = APIRouter(prefix="/appointments", tags=["Appointments"])


@router.post("")
def book_appointment(
    payload: AppointmentCreate,
    db: Session = Depends(get_db),
):
    # Verify doctor exists
    doctor = doctor_service.get_doctor_by_id(db, payload.doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    # Check conflict
    if appointment_service.check_conflict(
        db, payload.doctor_id, payload.appointment_date, payload.appointment_time
    ):
        alternatives = appointment_service.get_alternative_slots(
            db, payload.doctor_id, payload.appointment_date, payload.appointment_time
        )
        return {
            "message": "This slot is already booked. Please choose another time.",
            "available_alternative_slots": alternatives,
        }

    # Create appointment
    appt = appointment_service.create_appointment(
        db=db,
        doctor_id=payload.doctor_id,
        patient_name=payload.patient_name,
        patient_contact=payload.patient_contact,
        problem=payload.problem,
        appointment_date=payload.appointment_date,
        appointment_time=payload.appointment_time,
        consultation_type=payload.consultation_type,
    )

    # Send emails after DB write. Failures do not affect the saved appointment.
    doctor_email_sent = email_service.send_appointment_email(
        doctor_email=doctor.email,
        doctor_name=doctor.name,
        appointment_id=appt.id,
        patient_name=appt.patient_name,
        patient_contact=appt.patient_contact,
        problem=appt.problem,
        appointment_date=appt.appointment_date,
        appointment_time=appt.appointment_time,
        consultation_type=appt.consultation_type,
    )
    patient_email_sent = email_service.send_patient_appointment_confirmation(
        patient_email=appt.patient_contact,
        doctor_name=doctor.name,
        appointment_id=appt.id,
        patient_name=appt.patient_name,
        problem=appt.problem,
        appointment_date=appt.appointment_date,
        appointment_time=appt.appointment_time,
        consultation_type=appt.consultation_type,
    )

    return {
        "message": "Appointment booked successfully.",
        "appointment_id": appt.id,
        "status": appt.status,
        "email_sent": doctor_email_sent and patient_email_sent,
    }


@router.get("/doctor/{doctor_id}")
def get_doctor_appointments(doctor_id: int, db: Session = Depends(get_db)):
    appointments = appointment_service.get_doctor_appointments(db, doctor_id)
    return [AppointmentResponse.model_validate(a) for a in appointments]


@router.get("/{appointment_id}", response_model=AppointmentResponse)
def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appt = appointment_service.get_appointment_by_id(db, appointment_id)
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appt


@router.put("/{appointment_id}/status")
def update_status(
    appointment_id: int,
    payload: AppointmentStatusUpdate,
    db: Session = Depends(get_db),
):
    appt = appointment_service.update_appointment_status(db, appointment_id, payload.status)
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return {
        "appointment_id": appt.id,
        "status": appt.status,
        "message": "Status updated successfully.",
    }
