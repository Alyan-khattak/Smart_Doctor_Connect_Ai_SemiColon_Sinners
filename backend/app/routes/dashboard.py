from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import DashboardResponse, AppointmentResponse, ChatbotLeadResponse
from app.services import dashboard_service

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/doctor/{doctor_id}", response_model=DashboardResponse)
def get_doctor_dashboard(doctor_id: int, db: Session = Depends(get_db)):
    data = dashboard_service.get_dashboard(db, doctor_id)
    if not data:
        raise HTTPException(status_code=404, detail="Doctor not found")

    return DashboardResponse(
        doctor=data["doctor"],
        stats=data["stats"],
        appointments=[AppointmentResponse.model_validate(a) for a in data["appointments"]],
        chatbot_leads=[ChatbotLeadResponse.model_validate(l) for l in data["chatbot_leads"]],
    )
