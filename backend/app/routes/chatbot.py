from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import (
    ChatbotMessageRequest,
    ChatbotMessageResponse,
    ChatbotLeadCreate,
    ChatbotLeadResponse,
)
from app.services import chatbot_service, email_service, doctor_service

router = APIRouter(prefix="/chatbot", tags=["Chatbot"])


@router.post("/message", response_model=ChatbotMessageResponse)
def send_message(
    payload: ChatbotMessageRequest,
    db: Session = Depends(get_db),
):
    result = chatbot_service.process_message(
        db=db,
        doctor_id=payload.doctor_id,
        message=payload.message,
        state=payload.conversation_state,
        collected_data=payload.collected_data.model_dump(),
    )
    return result


@router.post("/lead")
def save_lead(
    payload: ChatbotLeadCreate,
    db: Session = Depends(get_db),
):
    # Get doctor for email
    doctor = doctor_service.get_doctor_by_id(db, payload.doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    # Save lead first (must succeed regardless of email)
    lead = chatbot_service.save_lead(
        db=db,
        doctor_id=payload.doctor_id,
        patient_name=payload.patient_name,
        patient_contact=payload.patient_contact,
        problem=payload.problem,
    )

    # Send lead notification email (non-blocking)
    email_sent = email_service.send_lead_email(
        doctor_email=doctor.email,
        doctor_name=doctor.name,
        lead_id=lead.id,
        patient_name=lead.patient_name,
        patient_contact=lead.patient_contact,
        problem=lead.problem,
    )

    return {
        "message": "Your details have been saved and the doctor has been notified.",
        "lead_id": lead.id,
        "email_sent": email_sent,
    }


@router.get("/leads/{doctor_id}")
def get_leads(doctor_id: int, db: Session = Depends(get_db)):
    leads = chatbot_service.get_doctor_leads(db, doctor_id)
    return [ChatbotLeadResponse.model_validate(l) for l in leads]
