from typing import Optional
from sqlalchemy.orm import Session
from app.models import Doctor


def get_all_doctors(db: Session):
    return db.query(Doctor).all()


def get_doctor_by_id(db: Session, doctor_id: int):
    return db.query(Doctor).filter(Doctor.id == doctor_id).first()


def search_doctors(
    db: Session,
    city: Optional[str] = None,
    specialization: Optional[str] = None,
    consultation_type: Optional[str] = None,
):
    query = db.query(Doctor)

    if city:
        query = query.filter(Doctor.city.ilike(f"%{city}%"))

    if specialization:
        query = query.filter(Doctor.specialization.ilike(f"%{specialization}%"))

    if consultation_type:
        query = query.filter(
            (Doctor.consultation_type == consultation_type)
            | (Doctor.consultation_type == "both")
        )

    return query.all()


def create_doctor(db: Session, data: dict):
    doctor = Doctor(**data)
    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    return doctor


def update_doctor(db: Session, doctor_id: int, data: dict):
    doctor = get_doctor_by_id(db, doctor_id)
    if not doctor:
        return None
    for key, value in data.items():
        if value is not None:
            setattr(doctor, key, value)
    db.commit()
    db.refresh(doctor)
    return doctor
