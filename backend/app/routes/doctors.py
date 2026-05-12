from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import DoctorCreate, DoctorUpdate, DoctorResponse, DoctorProfileCreate
from app.services import doctor_service, availability_service
from app.utils.security import get_current_doctor_auth
from app.models import DoctorAuth, Doctor

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

@router.get("/me/profile", response_model=DoctorResponse)
def get_my_profile(
    current_doctor_auth: DoctorAuth = Depends(get_current_doctor_auth),
    db: Session = Depends(get_db)
):
    doctor = db.query(Doctor).filter(Doctor.doctor_auth_id == current_doctor_auth.id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Profile not found")
    return doctor

@router.post("/me/profile", response_model=DoctorResponse, status_code=201)
def create_my_profile(
    payload: DoctorProfileCreate,
    current_doctor_auth: DoctorAuth = Depends(get_current_doctor_auth),
    db: Session = Depends(get_db)
):
    existing = db.query(Doctor).filter(Doctor.doctor_auth_id == current_doctor_auth.id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Profile already exists")
        
    doctor_data = payload.model_dump()
    doctor_data["name"] = current_doctor_auth.full_name
    doctor_data["email"] = current_doctor_auth.email
    doctor_data["doctor_auth_id"] = current_doctor_auth.id
    
    doctor = doctor_service.create_doctor(db, doctor_data)
    availability_service.ensure_profile_default_slots(db, doctor.id)
    return doctor

@router.put("/me/profile", response_model=DoctorResponse)
def update_my_profile(
    payload: DoctorUpdate,
    current_doctor_auth: DoctorAuth = Depends(get_current_doctor_auth),
    db: Session = Depends(get_db)
):
    doctor = db.query(Doctor).filter(Doctor.doctor_auth_id == current_doctor_auth.id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Profile not found")
        
    return doctor_service.update_doctor(
        db, doctor.id, payload.model_dump(exclude_none=True)
    )



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
