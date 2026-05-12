from datetime import date
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models import AvailabilitySlot

DEFAULT_SLOT_TIMES = ["17:00", "17:30", "18:00", "18:30", "19:00"]


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


def ensure_default_slots(db: Session, doctor_id: int, slot_date: str) -> List[AvailabilitySlot]:
    existing = get_slots(db, doctor_id, slot_date)
    if existing:
        return existing

    for slot_time in DEFAULT_SLOT_TIMES:
        db.add(
            AvailabilitySlot(
                doctor_id=doctor_id,
                slot_date=slot_date,
                slot_time=slot_time,
                is_booked=False,
            )
        )

    try:
        db.commit()
    except IntegrityError:
        db.rollback()

    return get_slots(db, doctor_id, slot_date)


def ensure_profile_default_slots(db: Session, doctor_id: int) -> None:
    ensure_default_slots(db, doctor_id, str(date.today()))
    ensure_default_slots(db, doctor_id, "2026-05-12")


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
