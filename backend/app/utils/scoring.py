"""
Doctor scoring formula from idea.md:

Specialization match = 50 points
City match           = 25 points
Available now        = 15 points
Consultation match   = 10 points
Rating bonus         = rating × 2
Experience bonus     = min(experience_years, 10)
"""

from app.models import Doctor


def score_doctor(
    doctor: Doctor,
    specialization: str,
    city: str | None,
    consultation_type: str | None,
) -> float:
    score = 0.0

    # Specialization match
    if doctor.specialization.lower() == specialization.lower():
        score += 50

    # City match
    if city and doctor.city.lower() == city.lower():
        score += 25

    # Availability
    if doctor.is_available:
        score += 15

    # Consultation type match
    if consultation_type:
        ct = consultation_type.lower()
        if doctor.consultation_type.lower() == ct:
            score += 10
        elif doctor.consultation_type.lower() == "both":
            # doctor supports both → still give partial match
            score += 10

    # Rating bonus
    if doctor.rating:
        score += doctor.rating * 2

    # Experience bonus (capped at 10)
    if doctor.experience_years:
        score += min(doctor.experience_years, 10)

    return round(score, 2)


def build_recommendation_reason(
    doctor: Doctor,
    specialization: str,
    city: str | None,
    consultation_type: str | None,
) -> str:
    parts = []

    if doctor.specialization.lower() == specialization.lower():
        parts.append(f"specialization matches {specialization}")

    if city and doctor.city.lower() == city.lower():
        parts.append(f"located in {doctor.city}")

    if doctor.is_available:
        parts.append("currently available")

    if consultation_type:
        ct = consultation_type.lower()
        if doctor.consultation_type.lower() == ct or doctor.consultation_type.lower() == "both":
            parts.append(f"supports {consultation_type} consultation")

    parts.append(f"rating {doctor.rating}/5")
    parts.append(f"{doctor.experience_years} years experience")

    reason = "Recommended because " + ", ".join(parts) + "."
    return reason
