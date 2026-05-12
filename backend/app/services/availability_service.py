from typing import List, Optional
from sqlalchemy.orm import Session
from app.models import AvailabilitySlot


def get_slots(db: Session, doctor_id: int, date: str) -> List[AvailabilitySlot]:
    return (
        db.query(AvailabilitySlot)
        .filter(
            AvailabilitySlot.doctor_id == doctor_id,
            AvailabilitySlot.slot_date == date,
        )
        .order_by(AvailabilitySlot.slot_time)
        .all()
    )


def get_earliest_available(slots: List[AvailabilitySlot]) -> Optional[str]:
    for slot in slots:
        if not slot.is_booked:
            return slot.slot_time
    return None


def create_slot(db: Session, doctor_id: int, slot_date: str, slot_time: str) -> AvailabilitySlot:
    slot = AvailabilitySlot(
        doctor_id=doctor_id,
        slot_date=slot_date,
        slot_time=slot_time,
        is_booked=False,
    )
    db.add(slot)
    db.commit()
    db.refresh(slot)
    return slot


def update_slot(db: Session, slot_id: int, is_booked: bool) -> Optional[AvailabilitySlot]:
    slot = db.query(AvailabilitySlot).filter(AvailabilitySlot.id == slot_id).first()
    if not slot:
        return None
    slot.is_booked = is_booked
    db.commit()
    db.refresh(slot)
    return slot


def get_available_slot_times(db: Session, doctor_id: int, date: str) -> List[str]:
    """Return times of unbooked slots for the given doctor and date."""
    slots = (
        db.query(AvailabilitySlot)
        .filter(
            AvailabilitySlot.doctor_id == doctor_id,
            AvailabilitySlot.slot_date == date,
            AvailabilitySlot.is_booked == False,
        )
        .order_by(AvailabilitySlot.slot_time)
        .all()
    )
    return [s.slot_time for s in slots]


def mark_slot_booked(db: Session, doctor_id: int, date: str, time: str) -> bool:
    slot = (
        db.query(AvailabilitySlot)
        .filter(
            AvailabilitySlot.doctor_id == doctor_id,
            AvailabilitySlot.slot_date == date,
            AvailabilitySlot.slot_time == time,
        )
        .first()
    )
    if slot:
        slot.is_booked = True
        db.commit()
        return True
    return False
