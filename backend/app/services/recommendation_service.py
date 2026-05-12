from typing import Optional, List
from sqlalchemy.orm import Session
from app.models import Doctor
from app.services import groq_service, doctor_service
from app.utils.scoring import score_doctor, build_recommendation_reason
from app.utils.constants import SAFETY_NOTE


def get_recommendations(
    db: Session,
    query: str,
    city: Optional[str],
    consultation_type: Optional[str],
) -> dict:
    """
    Full recommendation flow:
    1. Analyze query with Groq (or fallback)
    2. Search DB for matching doctors
    3. Score each doctor
    4. Sort by score descending
    5. Return top 5
    """
    # Step 1: Detect specialization
    groq_result = groq_service.analyze_symptoms(query)
    specialization = groq_result["specialization"]
    urgency = groq_result["urgency"]
    reason = groq_result["reason"]
    ai_used = groq_result["ai_used"]
    fallback_used = groq_result["fallback_used"]

    # Step 2: Fetch all doctors filtered by city (broad first, then score)
    all_doctors = db.query(Doctor).all()

    # Step 3: Score each doctor
    scored = []
    for doc in all_doctors:
        s = score_doctor(doc, specialization, city, consultation_type)
        rec_reason = build_recommendation_reason(doc, specialization, city, consultation_type)
        scored.append({
            "id": doc.id,
            "name": doc.name,
            "specialization": doc.specialization,
            "city": doc.city,
            "location": doc.location,
            "consultation_type": doc.consultation_type,
            "experience_years": doc.experience_years,
            "rating": doc.rating,
            "is_available": doc.is_available,
            "score": s,
            "recommendation_reason": rec_reason,
        })

    # Step 4: Sort by score descending, take top 5
    scored.sort(key=lambda x: x["score"], reverse=True)
    top_docs = scored[:5]

    return {
        "detected_specialization": specialization,
        "urgency": urgency,
        "ai_reason": reason,
        "recommended_doctors": top_docs,
        "safety_note": SAFETY_NOTE,
        "ai_used": ai_used,
        "fallback_used": fallback_used,
    }
