"""
Symptom keyword → specialization mapping.
Used as fallback when Groq AI is unavailable or returns invalid JSON.
"""

SYMPTOM_MAP: dict[str, str] = {
    # Orthopedic
    "back pain": "Orthopedic",
    "bone pain": "Orthopedic",
    "joint pain": "Orthopedic",
    "knee pain": "Orthopedic",
    "hip pain": "Orthopedic",
    "fracture": "Orthopedic",
    "spine": "Orthopedic",
    "arthritis": "Orthopedic",

    # Cardiology
    "chest pain": "Cardiologist",
    "heart": "Cardiologist",
    "shortness of breath": "Cardiologist",
    "palpitation": "Cardiologist",
    "high blood pressure": "Cardiologist",
    "hypertension": "Cardiologist",

    # Dermatology
    "skin": "Dermatologist",
    "rash": "Dermatologist",
    "acne": "Dermatologist",
    "allergy": "Dermatologist",
    "eczema": "Dermatologist",
    "itching": "Dermatologist",
    "hair loss": "Dermatologist",

    # Pediatrics
    "child": "Pediatrician",
    "baby": "Pediatrician",
    "infant": "Pediatrician",
    "kid": "Pediatrician",
    "fever in child": "Pediatrician",
    "vaccination": "Pediatrician",

    # Neurology
    "headache": "Neurologist",
    "migraine": "Neurologist",
    "seizure": "Neurologist",
    "dizziness": "Neurologist",
    "stroke": "Neurologist",
    "nerve": "Neurologist",

    # Gastroenterology
    "stomach pain": "Gastroenterologist",
    "abdominal pain": "Gastroenterologist",
    "diarrhea": "Gastroenterologist",
    "constipation": "Gastroenterologist",
    "acidity": "Gastroenterologist",
    "liver": "Gastroenterologist",
    "nausea": "Gastroenterologist",

    # ENT
    "ear pain": "ENT Specialist",
    "ear": "ENT Specialist",
    "nose": "ENT Specialist",
    "throat pain": "ENT Specialist",
    "tonsil": "ENT Specialist",
    "sinusitis": "ENT Specialist",
    "hearing loss": "ENT Specialist",

    # Ophthalmology
    "eye pain": "Ophthalmologist",
    "eye": "Ophthalmologist",
    "vision": "Ophthalmologist",
    "blurry": "Ophthalmologist",

    # Psychiatry
    "anxiety": "Psychiatrist",
    "depression": "Psychiatrist",
    "mental": "Psychiatrist",
    "stress": "Psychiatrist",
    "insomnia": "Psychiatrist",

    # Gynecology
    "pregnancy": "Gynecologist",
    "period": "Gynecologist",
    "menstrual": "Gynecologist",
    "ovarian": "Gynecologist",

    # Urology
    "kidney": "Urologist",
    "urinary": "Urologist",
    "bladder": "Urologist",
    "prostate": "Urologist",

    # Endocrinology
    "diabetes": "Endocrinologist",
    "thyroid": "Endocrinologist",
    "sugar": "Endocrinologist",

    # Pulmonology
    "cough": "Pulmonologist",
    "asthma": "Pulmonologist",
    "breathing": "Pulmonologist",
    "lung": "Pulmonologist",

    # Dentistry
    "tooth": "Dentist",
    "dental": "Dentist",
    "gum": "Dentist",
}

DEFAULT_SPECIALIZATION = "General Physician"

EMERGENCY_KEYWORDS = [
    "heart attack",
    "can't breathe",
    "cannot breathe",
    "unconscious",
    "severe bleeding",
    "emergency",
    "stroke",
    "chest crushing",
    "not breathing",
]


def detect_specialization_from_keywords(query: str) -> str:
    """Fallback: detect specialization using keyword matching."""
    query_lower = query.lower()
    for keyword, specialization in SYMPTOM_MAP.items():
        if keyword in query_lower:
            return specialization
    return DEFAULT_SPECIALIZATION


def is_emergency(message: str) -> bool:
    """Check if the message contains emergency keywords."""
    message_lower = message.lower()
    return any(kw in message_lower for kw in EMERGENCY_KEYWORDS)
