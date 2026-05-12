import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from app.config import settings

logger = logging.getLogger(__name__)


def _smtp_enabled() -> bool:
    if not settings.ENABLE_EMAIL:
        logger.info("ENABLE_EMAIL is false; SMTP email sending skipped.")
        return False

    missing = [
        name
        for name, value in {
            "SMTP_HOST": settings.SMTP_HOST,
            "SMTP_USERNAME": settings.SMTP_USERNAME,
            "SMTP_PASSWORD": settings.SMTP_PASSWORD,
            "SMTP_FROM_EMAIL": settings.SMTP_FROM_EMAIL,
        }.items()
        if not value
    ]
    if missing:
        logger.warning("SMTP email skipped; missing config: %s", ", ".join(missing))
        return False

    return True


def _send_smtp_email(to_email: str, subject: str, html: str, text: str) -> bool:
    if not _smtp_enabled():
        return False

    if not to_email:
        logger.warning("SMTP email skipped; recipient email is empty.")
        return False

    try:
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = f"{settings.SMTP_FROM_NAME} <{settings.SMTP_FROM_EMAIL}>"
        message["To"] = to_email
        message.attach(MIMEText(text, "plain"))
        message.attach(MIMEText(html, "html"))

        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=20) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
            server.sendmail(settings.SMTP_FROM_EMAIL, [to_email], message.as_string())

        return True
    except Exception:
        logger.exception("SMTP email failed")
        return False


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
    Send appointment notification email to doctor via SMTP.
    Returns True on success, False on failure.
    Email failure must NOT break the appointment booking.
    """
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
    text = f"""New Appointment Booked

Appointment ID: #{appointment_id}
Doctor: {doctor_name}
Patient Name: {patient_name}
Contact: {patient_contact}
Problem: {problem}
Date: {appointment_date}
Time: {appointment_time}
Consultation Type: {consultation_type}

Please log in to your Smart Doctor Connect AI dashboard to manage this appointment.
"""

    sent = _send_smtp_email(
        to_email=doctor_email,
        subject=f"New Appointment from {patient_name} — Smart Doctor Connect AI",
        html=html,
        text=text,
    )
    if sent:
        logger.info(f"Appointment email sent for appointment #{appointment_id}")
    return sent


def send_lead_email(
    doctor_email: str,
    doctor_name: str,
    lead_id: int,
    patient_name: str,
    patient_contact: str,
    problem: str,
) -> bool:
    """
    Send chatbot lead notification email to doctor via SMTP.
    Returns True on success, False on failure.
    Email failure must NOT delete the saved lead.
    """
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
    text = f"""New Patient Lead from AI Chatbot

Lead ID: #{lead_id}
Doctor: {doctor_name}
Patient Name: {patient_name}
Contact: {patient_contact}
Problem: {problem}

This patient tried to contact you when you were unavailable. Please follow up as soon as possible.
Check your Smart Doctor Connect AI dashboard for more details.
"""

    sent = _send_smtp_email(
        to_email=doctor_email,
        subject=f"New Patient Lead: {patient_name} — Smart Doctor Connect AI",
        html=html,
        text=text,
    )
    if sent:
        logger.info(f"Lead email sent for lead #{lead_id}")
    return sent


def send_patient_appointment_confirmation(
    patient_email: str,
    doctor_name: str,
    appointment_id: int,
    patient_name: str,
    problem: str,
    appointment_date: str,
    appointment_time: str,
    consultation_type: str,
) -> bool:
    """
    Send appointment confirmation email to the patient via SMTP.
    The appointment remains saved even if this notification fails.
    """
    html = f"""
    <h2>Appointment Request Received</h2>
    <p>Hello {patient_name},</p>
    <p>Your appointment request has been saved.</p>
    <table style="border-collapse:collapse; width:100%;">
      <tr><td style="padding:8px; border:1px solid #ddd;"><strong>Appointment ID</strong></td><td style="padding:8px; border:1px solid #ddd;">#{appointment_id}</td></tr>
      <tr><td style="padding:8px; border:1px solid #ddd;"><strong>Doctor</strong></td><td style="padding:8px; border:1px solid #ddd;">{doctor_name}</td></tr>
      <tr><td style="padding:8px; border:1px solid #ddd;"><strong>Problem</strong></td><td style="padding:8px; border:1px solid #ddd;">{problem}</td></tr>
      <tr><td style="padding:8px; border:1px solid #ddd;"><strong>Date</strong></td><td style="padding:8px; border:1px solid #ddd;">{appointment_date}</td></tr>
      <tr><td style="padding:8px; border:1px solid #ddd;"><strong>Time</strong></td><td style="padding:8px; border:1px solid #ddd;">{appointment_time}</td></tr>
      <tr><td style="padding:8px; border:1px solid #ddd;"><strong>Type</strong></td><td style="padding:8px; border:1px solid #ddd;">{consultation_type}</td></tr>
    </table>
    <p>The doctor's clinic has been notified.</p>
    """
    text = f"""Appointment Request Received

Hello {patient_name},

Your appointment request has been saved.

Appointment ID: #{appointment_id}
Doctor: {doctor_name}
Problem: {problem}
Date: {appointment_date}
Time: {appointment_time}
Consultation Type: {consultation_type}

The doctor's clinic has been notified.
"""

    sent = _send_smtp_email(
        to_email=patient_email,
        subject=f"Appointment Request Received — Smart Doctor Connect AI",
        html=html,
        text=text,
    )
    if sent:
        logger.info(f"Patient appointment email sent for appointment #{appointment_id}")
    return sent
