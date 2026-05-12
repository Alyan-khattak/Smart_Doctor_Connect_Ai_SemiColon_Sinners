from datetime import date as date_type
from sqlalchemy.orm import Session
from app.models import Doctor, Appointment, ChatbotLead


def get_dashboard(db: Session, doctor_id: int) -> dict | None:
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        return None

    today_str = str(date_type.today())

    all_appts = (
        db.query(Appointment)
        .filter(Appointment.doctor_id == doctor_id)
        .order_by(Appointment.appointment_date.desc())
        .all()
    )

    total_appointments = len(all_appts)
    pending_appointments = sum(1 for a in all_appts if a.status == "pending")
    today_appointments = sum(1 for a in all_appts if a.appointment_date == today_str)

    leads = (
        db.query(ChatbotLead)
        .filter(ChatbotLead.doctor_id == doctor_id)
        .order_by(ChatbotLead.created_at.desc())
        .all()
    )

    new_chatbot_leads = sum(1 for l in leads if l.status == "new")

    return {
        "doctor": {
            "id": doctor.id,
            "name": doctor.name,
            "specialization": doctor.specialization,
            "city": doctor.city,
            "is_available": doctor.is_available,
        },
        "stats": {
            "total_appointments": total_appointments,
            "pending_appointments": pending_appointments,
            "today_appointments": today_appointments,
            "new_chatbot_leads": new_chatbot_leads,
        },
        "appointments": all_appts,
        "chatbot_leads": leads,
    }
