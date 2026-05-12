from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import AvailabilityCreate, AvailabilityUpdate, AvailabilitySlotResponse, AvailabilityResponse
from app.services import availability_service

router = APIRouter(prefix="/availability", tags=["Availability"])


@router.get("/{doctor_id}", response_model=AvailabilityResponse)
def get_availability(
    doctor_id: int,
    date: str,
    db: Session = Depends(get_db),
):
    slots = availability_service.ensure_default_slots(db, doctor_id, date)
    earliest = availability_service.get_earliest_available(slots)

    slot_list = [
        AvailabilitySlotResponse(
            slot_id=s.id,
            time=s.slot_time,
            is_booked=s.is_booked,
        )
        for s in slots
    ]

    return AvailabilityResponse(
        doctor_id=doctor_id,
        date=date,
        slots=slot_list,
        earliest_available_slot=earliest,
    )


@router.post("/{doctor_id}", status_code=201)
def add_slot(
    doctor_id: int,
    payload: AvailabilityCreate,
    db: Session = Depends(get_db),
):
    slot = availability_service.create_slot(
        db, doctor_id, payload.slot_date, payload.slot_time
    )
    return {
        "slot_id": slot.id,
        "doctor_id": doctor_id,
        "slot_date": slot.slot_date,
        "slot_time": slot.slot_time,
        "is_booked": slot.is_booked,
    }


@router.put("/slot/{slot_id}")
def update_slot(
    slot_id: int,
    payload: AvailabilityUpdate,
    db: Session = Depends(get_db),
):
    slot = availability_service.update_slot(db, slot_id, payload.is_booked)
    if not slot:
        raise HTTPException(status_code=404, detail="Slot not found")
    return {
        "slot_id": slot.id,
        "is_booked": slot.is_booked,
    }
