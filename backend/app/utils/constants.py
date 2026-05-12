"""
Shared backend constants.
"""

# Appointment statuses
APPOINTMENT_STATUSES = ["pending", "confirmed", "cancelled", "completed"]

# Consultation types
CONSULTATION_TYPES = ["online", "physical", "both"]

# Chatbot conversation states
CHATBOT_STATES = [
    "START",
    "ASK_NAME",
    "ASK_CONTACT",
    "ASK_PROBLEM",
    "CONFIRM_DETAILS",
    "SAVE_LEAD",
    "SEND_EMAIL",
    "END",
]

# Default time slots per day
DEFAULT_TIME_SLOTS = [
    "17:00",
    "17:30",
    "18:00",
    "18:30",
    "19:00",
    "19:30",
    "20:00",
]

# Safety note (must appear in recommendation responses)
SAFETY_NOTE = (
    "This system helps find doctors. "
    "It does not provide diagnosis or emergency medical care."
)

# Emergency response
EMERGENCY_REPLY = (
    "This may be a medical emergency. "
    "Please call emergency services (Rescue 1122 in Pakistan) immediately. "
    "This AI assistant cannot provide emergency care."
)
