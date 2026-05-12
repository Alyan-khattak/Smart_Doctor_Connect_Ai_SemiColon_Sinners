"""
Pytest configuration and shared fixtures.
Uses a separate in-memory SQLite DB for tests.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app

TEST_DATABASE_URL = "sqlite:///./test_smart_doctor.db"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=test_engine)
    session = TestSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def seeded_client(client, db_session):
    """Client with one seeded doctor."""
    from app.models import Doctor, AvailabilitySlot

    doc = Doctor(
        name="Dr. Test Doctor",
        email="test@example.com",
        specialization="Orthopedic",
        city="Lahore",
        location="Test Clinic",
        consultation_type="both",
        experience_years=5,
        rating=4.5,
        is_available=True,
        bio="Test doctor bio",
    )
    db_session.add(doc)
    db_session.commit()
    db_session.refresh(doc)

    from datetime import date
    today = str(date.today())
    for t in ["17:00", "17:30", "18:00", "18:30", "19:00"]:
        slot = AvailabilitySlot(
            doctor_id=doc.id,
            slot_date=today,
            slot_time=t,
            is_booked=False,
        )
        db_session.add(slot)
    db_session.commit()

    yield client, doc
