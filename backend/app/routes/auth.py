from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.models import DoctorAuth, Doctor
from app.schemas import DoctorAuthCreate, Token, DoctorProfileCreate, DoctorResponse
from app.utils.security import get_password_hash, verify_password, create_access_token, get_current_doctor_auth

router = APIRouter(prefix="/auth/doctor", tags=["doctor auth"])

@router.post("/register", response_model=Token)
def register_doctor(doctor: DoctorAuthCreate, db: Session = Depends(get_db)):
    # Check if doctor already exists
    existing = db.query(DoctorAuth).filter(DoctorAuth.email == doctor.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    hashed_password = get_password_hash(doctor.password)
    new_doctor_auth = DoctorAuth(
        email=doctor.email,
        password_hash=hashed_password,
        full_name=doctor.full_name
    )
    
    try:
        db.add(new_doctor_auth)
        db.commit()
        db.refresh(new_doctor_auth)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not create user"
        )
        
    access_token = create_access_token(data={"sub": new_doctor_auth.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
def login_doctor(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    doctor_auth = db.query(DoctorAuth).filter(DoctorAuth.email == form_data.username).first()
    if not doctor_auth or not verify_password(form_data.password, doctor_auth.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token = create_access_token(data={"sub": doctor_auth.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=dict)
def get_doctor_me(current_doctor_auth: DoctorAuth = Depends(get_current_doctor_auth), db: Session = Depends(get_db)):
    # Find if this auth account has a linked profile
    profile = db.query(Doctor).filter(Doctor.doctor_auth_id == current_doctor_auth.id).first()
    return {
        "auth": {
            "id": current_doctor_auth.id,
            "email": current_doctor_auth.email,
            "full_name": current_doctor_auth.full_name,
        },
        "has_profile": profile is not None,
        "profile_id": profile.id if profile else None
    }
