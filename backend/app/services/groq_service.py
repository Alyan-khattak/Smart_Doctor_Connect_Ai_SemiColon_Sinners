import json
import logging
from typing import Optional
from app.config import settings
from app.utils.symptom_map import detect_specialization_from_keywords

logger = logging.getLogger(__name__)


def analyze_symptoms(query: str) -> dict:
    """
    Call Groq to detect specialization, urgency, and reason from patient query.
    Returns dict with: specialization, urgency, reason, ai_used, fallback_used
    Falls back to keyword matching if Groq fails or returns invalid JSON.
    """
    if not settings.GROQ_API_KEY:
        logger.warning("GROQ_API_KEY not set — using keyword fallback.")
        return _keyword_fallback(query)

    try:
        from groq import Groq

        client = Groq(api_key=settings.GROQ_API_KEY)

        prompt = f"""You are a medical specialization assistant for a Pakistani healthcare app.
Analyze the following patient query and return ONLY valid JSON with these exact fields:
- specialization: the recommended medical specialization (e.g., "Orthopedic", "Cardiologist", "Dermatologist", "Pediatrician", "Neurologist", "Gastroenterologist", "General Physician", "ENT Specialist", "Ophthalmologist", "Psychiatrist", "Gynecologist", "Urologist", "Endocrinologist", "Pulmonologist", "Dentist")
- urgency: "low", "medium", or "high"
- reason: one sentence explaining why this specialization matches

Patient query: "{query}"

Respond with ONLY this JSON structure, no other text:
{{"specialization": "...", "urgency": "...", "reason": "..."}}"""

        response = client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=200,
        )

        content = response.choices[0].message.content.strip()

        # Try to extract JSON if Groq wrapped it
        if "```" in content:
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
            content = content.strip()

        result = json.loads(content)

        return {
            "specialization": result.get("specialization", "General Physician"),
            "urgency": result.get("urgency", "medium"),
            "reason": result.get("reason", ""),
            "ai_used": True,
            "fallback_used": False,
        }

    except Exception as e:
        logger.warning(f"Groq failed: {e} — using keyword fallback.")
        return _keyword_fallback(query)


def _keyword_fallback(query: str) -> dict:
    specialization = detect_specialization_from_keywords(query)
    return {
        "specialization": specialization,
        "urgency": "medium",
        "reason": f"Based on keyword analysis, {specialization} is recommended.",
        "ai_used": False,
        "fallback_used": True,
    }


def generate_chatbot_reply(
    doctor_name: str,
    message: str,
    state: str,
    collected_data: dict,
) -> str:
    """
    Generate AI chatbot response using Groq.
    Falls back to deterministic replies if Groq fails.
    """
    if not settings.GROQ_API_KEY:
        return _deterministic_chatbot_reply(doctor_name, state, collected_data)

    try:
        from groq import Groq

        client = Groq(api_key=settings.GROQ_API_KEY)

        collected_str = json.dumps(collected_data, indent=2)

        prompt = f"""You are a helpful AI assistant for Dr. {doctor_name}'s clinic. 
The doctor is currently unavailable. You are collecting patient information.

Current conversation state: {state}
Patient message: "{message}"
Information collected so far: {collected_str}

Rules:
- NEVER provide medical diagnosis or prescribe medicine
- NEVER claim to be a real doctor
- Be warm, professional, and concise (max 2 sentences)
- Based on state, ask for the next piece of information:
  - START or ASK_NAME: Ask for patient's full name
  - ASK_CONTACT: Ask for patient's phone number
  - ASK_PROBLEM: Ask patient to describe their medical concern briefly
  - CONFIRM_DETAILS: Confirm all collected details and say doctor will be notified

Respond with only your reply text, no JSON."""

        response = client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=150,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        logger.warning(f"Groq chatbot failed: {e} — using deterministic reply.")
        return _deterministic_chatbot_reply(doctor_name, state, collected_data)


def _deterministic_chatbot_reply(doctor_name: str, state: str, collected_data: dict) -> str:
    """Fallback deterministic chatbot replies."""
    replies = {
        "START": f"Dr. {doctor_name} is currently unavailable. I'm the AI assistant. Could you please share your full name so I can notify the doctor?",
        "ASK_NAME": "Thank you! Could you please provide your contact number (phone) so the doctor can reach you?",
        "ASK_CONTACT": "Got it! Please briefly describe your medical concern or symptoms.",
        "ASK_PROBLEM": f"Thank you for sharing that. Let me confirm your details: Name: {collected_data.get('patient_name')}, Contact: {collected_data.get('patient_contact')}, Problem: {collected_data.get('problem')}. I'll notify Dr. {doctor_name} right away.",
        "CONFIRM_DETAILS": "Your information has been saved. The doctor will contact you as soon as possible.",
    }
    return replies.get(state, f"I'm here to help connect you with Dr. {doctor_name}. The doctor will be notified of your inquiry.")
