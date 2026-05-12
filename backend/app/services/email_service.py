import logging
from typing import Optional
from app.config import settings

logger = logging.getLogger(__name__)


def send_appointment_email(
    doctor_email: str,
    doctor_name: str,
    appointment_id: int,
    patient_name: str,
    patient_contact: str,
    problem: str,
    appointment_date: str,
    appointment_time: str,
    consultation_type: str,
) -> bool:
    """
    Send appointment notification email to doctor via Resend.
    Returns True on success, False on failure.
    Email failure must NOT break the appointment booking.
    """
    if not settings.RESEND_API_KEY:
        logger.warning("RESEND_API_KEY not set — email skipped.")
        return False

    try:
        import resend

        resend.api_key = settings.RESEND_API_KEY

        to_email = settings.RESEND_TEST_TO or doctor_email

        html = f"""
        <h2>New Appointment Booked</h2>
        <p><strong>Appointment ID:</strong> #{appointment_id}</p>
        <table style="border-collapse:collapse; width:100%;">
          <tr><td style="padding:8px; border:1px solid #ddd;"><strong>Patient Name</strong></td><td style="padding:8px; border:1px solid #ddd;">{patient_name}</td></tr>
          <tr><td style="padding:8px; border:1px solid #ddd;"><strong>Contact</strong></td><td style="padding:8px; border:1px solid #ddd;">{patient_contact}</td></tr>
          <tr><td style="padding:8px; border:1px solid #ddd;"><strong>Problem</strong></td><td style="padding:8px; border:1px solid #ddd;">{problem}</td></tr>
          <tr><td style="padding:8px; border:1px solid #ddd;"><strong>Date</strong></td><td style="padding:8px; border:1px solid #ddd;">{appointment_date}</td></tr>
          <tr><td style="padding:8px; border:1px solid #ddd;"><strong>Time</strong></td><td style="padding:8px; border:1px solid #ddd;">{appointment_time}</td></tr>
          <tr><td style="padding:8px; border:1px solid #ddd;"><strong>Type</strong></td><td style="padding:8px; border:1px solid #ddd;">{consultation_type}</td></tr>
        </table>
        <p>Please log in to your Smart Doctor Connect AI dashboard to manage this appointment.</p>
        """

        params = {
            "from": settings.RESEND_FROM_EMAIL,
            "to": [to_email],
            "subject": f"New Appointment from {patient_name} — Smart Doctor Connect AI",
            "html": html,
        }

        resend.Emails.send(params)
        logger.info(f"Appointment email sent for appointment #{appointment_id}")
        return True

    except Exception as e:
        logger.error(f"Resend appointment email failed: {e}")
        return False


def send_lead_email(
    doctor_email: str,
    doctor_name: str,
    lead_id: int,
    patient_name: str,
    patient_contact: str,
    problem: str,
) -> bool:
    """
    Send chatbot lead notification email to doctor via Resend.
    Returns True on success, False on failure.
    Email failure must NOT delete the saved lead.
    """
    if not settings.RESEND_API_KEY:
        logger.warning("RESEND_API_KEY not set — lead email skipped.")
        return False

    try:
        import resend

        resend.api_key = settings.RESEND_API_KEY

        to_email = settings.RESEND_TEST_TO or doctor_email

        html = f"""
        <h2>New Patient Lead from AI Chatbot</h2>
        <p><strong>Lead ID:</strong> #{lead_id}</p>
        <table style="border-collapse:collapse; width:100%;">
          <tr><td style="padding:8px; border:1px solid #ddd;"><strong>Patient Name</strong></td><td style="padding:8px; border:1px solid #ddd;">{patient_name}</td></tr>
          <tr><td style="padding:8px; border:1px solid #ddd;"><strong>Contact</strong></td><td style="padding:8px; border:1px solid #ddd;">{patient_contact}</td></tr>
          <tr><td style="padding:8px; border:1px solid #ddd;"><strong>Problem</strong></td><td style="padding:8px; border:1px solid #ddd;">{problem}</td></tr>
        </table>
        <p>This patient tried to contact you when you were unavailable. Please follow up as soon as possible.</p>
        <p>Check your Smart Doctor Connect AI dashboard for more details.</p>
        """

        params = {
            "from": settings.RESEND_FROM_EMAIL,
            "to": [to_email],
            "subject": f"New Patient Lead: {patient_name} — Smart Doctor Connect AI",
            "html": html,
        }

        resend.Emails.send(params)
        logger.info(f"Lead email sent for lead #{lead_id}")
        return True

    except Exception as e:
        logger.error(f"Resend lead email failed: {e}")
        return False
