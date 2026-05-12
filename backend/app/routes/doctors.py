from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import DoctorCreate, DoctorUpdate, DoctorResponse
from app.services import doctor_service

router = APIRouter(prefix="/doctors", tags=["Doctors"])


# IMPORTANT: /search must come before /{doctor_id} to avoid route conflict
@router.get("/search", response_model=dict)
def search_doctors(
    city: Optional[str] = None,
    specialization: Optional[str] = None,
    consultation_type: Optional[str] = None,
    db: Session = Depends(get_db),
):
    results = doctor_service.search_doctors(db, city, specialization, consultation_type)
    return {"results": [DoctorResponse.model_validate(d) for d in results]}


@router.get("", response_model=List[DoctorResponse])
def get_all_doctors(db: Session = Depends(get_db)):
    return doctor_service.get_all_doctors(db)


@router.get("/{doctor_id}", response_model=DoctorResponse)
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor = doctor_service.get_doctor_by_id(db, doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor


@router.post("", response_model=DoctorResponse, status_code=201)
def create_doctor(payload: DoctorCreate, db: Session = Depends(get_db)):
    return doctor_service.create_doctor(db, payload.model_dump())


@router.put("/{doctor_id}", response_model=DoctorResponse)
def update_doctor(doctor_id: int, payload: DoctorUpdate, db: Session = Depends(get_db)):
    doctor = doctor_service.update_doctor(
        db, doctor_id, payload.model_dump(exclude_none=True)
    )
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor
