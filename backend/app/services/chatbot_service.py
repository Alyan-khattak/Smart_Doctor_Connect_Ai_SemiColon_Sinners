from typing import Optional, List
from sqlalchemy.orm import Session
from app.models import ChatbotLead
from app.services import groq_service, doctor_service
from app.utils.symptom_map import is_emergency
from app.utils.constants import EMERGENCY_REPLY


def process_message(
    db: Session,
    doctor_id: int,
    message: str,
    state: str,
    collected_data: dict,
) -> dict:
    """
    Chatbot state machine.
    Returns: reply, next_state, collected_data, is_complete
    """

    # Emergency check — always first
    if is_emergency(message):
        return {
            "reply": EMERGENCY_REPLY,
            "next_state": "END",
            "collected_data": collected_data,
            "is_complete": False,
        }

    doctor = doctor_service.get_doctor_by_id(db, doctor_id)
    doctor_name = doctor.name if doctor else "the doctor"

    # Collect data based on state
    updated_data = dict(collected_data)
    next_state = state

    if state == "START":
        next_state = "ASK_NAME"

    elif state == "ASK_NAME":
        if message.strip():
            updated_data["patient_name"] = message.strip()
            next_state = "ASK_CONTACT"

    elif state == "ASK_CONTACT":
        if message.strip():
            updated_data["patient_contact"] = message.strip()
            next_state = "ASK_PROBLEM"

    elif state == "ASK_PROBLEM":
        if message.strip():
            updated_data["problem"] = message.strip()
            next_state = "CONFIRM_DETAILS"

    elif state in ("CONFIRM_DETAILS", "SAVE_LEAD", "SEND_EMAIL"):
        next_state = "END"

    # Generate AI reply
    reply = groq_service.generate_chatbot_reply(
        doctor_name=doctor_name,
        message=message,
        state=next_state,
        collected_data=updated_data,
    )

    is_complete = (
        updated_data.get("patient_name")
        and updated_data.get("patient_contact")
        and updated_data.get("problem")
        and next_state == "CONFIRM_DETAILS"
    )

    return {
        "reply": reply,
        "next_state": next_state,
        "collected_data": updated_data,
        "is_complete": bool(is_complete),
    }


def save_lead(
    db: Session,
    doctor_id: int,
    patient_name: str,
    patient_contact: str,
    problem: str,
) -> ChatbotLead:
    lead = ChatbotLead(
        doctor_id=doctor_id,
        patient_name=patient_name,
        patient_contact=patient_contact,
        problem=problem,
        status="new",
    )
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return lead


def get_doctor_leads(db: Session, doctor_id: int) -> List[ChatbotLead]:
    return (
        db.query(ChatbotLead)
        .filter(ChatbotLead.doctor_id == doctor_id)
        .order_by(ChatbotLead.created_at.desc())
        .all()
    )
