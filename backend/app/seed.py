"""
Seed script — creates 15 Pakistani doctors and availability slots.
Run: python -m app.seed
"""

from app.database import SessionLocal, engine, Base
from app.models import Doctor, AvailabilitySlot
from app.utils.constants import DEFAULT_TIME_SLOTS
from datetime import date, timedelta

Base.metadata.create_all(bind=engine)

DOCTORS = [
    {
        "name": "Dr. Sara Malik",
        "email": "sara.malik@example.com",
        "specialization": "Orthopedic",
        "city": "Lahore",
        "location": "Johar Town Clinic",
        "consultation_type": "both",
        "experience_years": 8,
        "rating": 4.8,
        "is_available": True,
        "bio": "Experienced orthopedic specialist for bone, joint, and back pain.",
    },
    {
        "name": "Dr. Hamza Ali",
        "email": "hamza.ali@example.com",
        "specialization": "Cardiologist",
        "city": "Lahore",
        "location": "Gulberg Heart Center",
        "consultation_type": "online",
        "experience_years": 12,
        "rating": 4.9,
        "is_available": False,
        "bio": "Senior cardiologist with expertise in heart disease and hypertension.",
    },
    {
        "name": "Dr. Ayesha Khan",
        "email": "ayesha.khan@example.com",
        "specialization": "Dermatologist",
        "city": "Karachi",
        "location": "DHA Skin Clinic",
        "consultation_type": "both",
        "experience_years": 6,
        "rating": 4.7,
        "is_available": True,
        "bio": "Specialist in skin diseases, acne, and cosmetic dermatology.",
    },
    {
        "name": "Dr. Usman Tariq",
        "email": "usman.tariq@example.com",
        "specialization": "Neurologist",
        "city": "Islamabad",
        "location": "F-7 Neurology Center",
        "consultation_type": "physical",
        "experience_years": 10,
        "rating": 4.6,
        "is_available": True,
        "bio": "Neurology specialist for headaches, migraines, and nerve disorders.",
    },
    {
        "name": "Dr. Fatima Zahra",
        "email": "fatima.zahra@example.com",
        "specialization": "Pediatrician",
        "city": "Karachi",
        "location": "Clifton Children's Clinic",
        "consultation_type": "both",
        "experience_years": 9,
        "rating": 4.9,
        "is_available": True,
        "bio": "Pediatric care specialist for infants, children, and adolescents.",
    },
    {
        "name": "Dr. Bilal Ahmed",
        "email": "bilal.ahmed@example.com",
        "specialization": "Gastroenterologist",
        "city": "Lahore",
        "location": "Model Town Gastro Clinic",
        "consultation_type": "physical",
        "experience_years": 7,
        "rating": 4.5,
        "is_available": True,
        "bio": "Expert in stomach, liver, and digestive system disorders.",
    },
    {
        "name": "Dr. Nadia Hussain",
        "email": "nadia.hussain@example.com",
        "specialization": "Gynecologist",
        "city": "Islamabad",
        "location": "G-9 Women's Health Center",
        "consultation_type": "physical",
        "experience_years": 11,
        "rating": 4.8,
        "is_available": True,
        "bio": "Women's health specialist with expertise in pregnancy and reproductive health.",
    },
    {
        "name": "Dr. Kamran Sheikh",
        "email": "kamran.sheikh@example.com",
        "specialization": "Orthopedic",
        "city": "Karachi",
        "location": "Saddar Orthopedic Hospital",
        "consultation_type": "both",
        "experience_years": 14,
        "rating": 4.7,
        "is_available": False,
        "bio": "Orthopedic surgeon specializing in sports injuries and joint replacements.",
    },
    {
        "name": "Dr. Zara Siddiqui",
        "email": "zara.siddiqui@example.com",
        "specialization": "Psychiatrist",
        "city": "Lahore",
        "location": "Gulberg Mental Wellness Center",
        "consultation_type": "online",
        "experience_years": 5,
        "rating": 4.6,
        "is_available": True,
        "bio": "Psychiatrist offering online therapy for anxiety, depression, and stress.",
    },
    {
        "name": "Dr. Asad Raza",
        "email": "asad.raza@example.com",
        "specialization": "ENT Specialist",
        "city": "Peshawar",
        "location": "Hayatabad ENT Clinic",
        "consultation_type": "physical",
        "experience_years": 8,
        "rating": 4.5,
        "is_available": True,
        "bio": "ENT specialist for ear, nose, and throat conditions including sinusitis.",
    },
    {
        "name": "Dr. Mehwish Iqbal",
        "email": "mehwish.iqbal@example.com",
        "specialization": "Endocrinologist",
        "city": "Lahore",
        "location": "DHA Diabetes Clinic",
        "consultation_type": "both",
        "experience_years": 9,
        "rating": 4.7,
        "is_available": True,
        "bio": "Specialist in diabetes, thyroid disorders, and hormonal conditions.",
    },
    {
        "name": "Dr. Tariq Mehmood",
        "email": "tariq.mehmood@example.com",
        "specialization": "Pulmonologist",
        "city": "Rawalpindi",
        "location": "Satellite Town Lung Clinic",
        "consultation_type": "physical",
        "experience_years": 13,
        "rating": 4.8,
        "is_available": True,
        "bio": "Lung and respiratory specialist for asthma, COPD, and chest infections.",
    },
    {
        "name": "Dr. Sana Farooq",
        "email": "sana.farooq@example.com",
        "specialization": "Ophthalmologist",
        "city": "Karachi",
        "location": "Korangi Eye Care Center",
        "consultation_type": "physical",
        "experience_years": 7,
        "rating": 4.6,
        "is_available": True,
        "bio": "Eye specialist treating vision disorders, cataracts, and retinal conditions.",
    },
    {
        "name": "Dr. Imran Chaudhry",
        "email": "imran.chaudhry@example.com",
        "specialization": "Urologist",
        "city": "Faisalabad",
        "location": "Peoples Colony Urology Center",
        "consultation_type": "both",
        "experience_years": 10,
        "rating": 4.5,
        "is_available": True,
        "bio": "Urology specialist for kidney stones, UTIs, and prostate conditions.",
    },
    {
        "name": "Dr. Raheela Nasir",
        "email": "raheela.nasir@example.com",
        "specialization": "General Physician",
        "city": "Multan",
        "location": "Bosan Road Family Clinic",
        "consultation_type": "both",
        "experience_years": 6,
        "rating": 4.4,
        "is_available": True,
        "bio": "General physician for routine checkups, fever, and common ailments.",
    },
]


def seed():
    db = SessionLocal()

    try:
        # Skip if already seeded
        if db.query(Doctor).count() >= len(DOCTORS):
            print("Database already seeded. Skipping.")
            return

        # Seed doctors
        doctor_records = []
        for d in DOCTORS:
            doc = Doctor(**d)
            db.add(doc)
            doctor_records.append(doc)

        db.commit()

        # Refresh to get IDs
        for doc in doctor_records:
            db.refresh(doc)

        # Seed availability slots for next 7 days
        today = date.today()
        slot_count = 0

        for doc in doctor_records:
            for day_offset in range(7):
                slot_date = str(today + timedelta(days=day_offset))
                for slot_time in DEFAULT_TIME_SLOTS:
                    # Skip if already exists
                    existing = (
                        db.query(AvailabilitySlot)
                        .filter(
                            AvailabilitySlot.doctor_id == doc.id,
                            AvailabilitySlot.slot_date == slot_date,
                            AvailabilitySlot.slot_time == slot_time,
                        )
                        .first()
                    )
                    if not existing:
                        slot = AvailabilitySlot(
                            doctor_id=doc.id,
                            slot_date=slot_date,
                            slot_time=slot_time,
                            is_booked=False,
                        )
                        db.add(slot)
                        slot_count += 1

        db.commit()

        print(f"[OK] Seeded {len(doctor_records)} doctors and {slot_count} availability slots.")

    except Exception as e:
        db.rollback()
        print(f"[ERROR] Seed failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
