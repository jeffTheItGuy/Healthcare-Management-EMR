"""Generic input validators."""
import re
from typing import Optional


def validate_national_id(national_id: Optional[str]) -> bool:
    """Validate a national ID. Accepts alphanumeric + dashes, 5-30 chars."""
    if not national_id:
        return True  # Optional field
    cleaned = national_id.strip().upper()
    return bool(re.match(r"^[A-Z0-9\-]{5,30}$", cleaned))


def validate_phone(phone: Optional[str]) -> bool:
    """Validate a phone number. Accepts 7-15 digits, optional leading '+'."""
    if not phone:
        return True  # Optional field
    cleaned = re.sub(r"[\s\-()]", "", phone.strip())
    return bool(re.match(r"^\+?\d{7,15}$", cleaned))


def validate_patient_number(patient_number: str) -> bool:
    """Validate patient number format: P-YYYY-NNNNNN"""
    if not patient_number:
        return False
    return bool(re.match(r"^P-\d{4}-\d{6}$", patient_number.strip().upper()))


def generate_patient_number(year: int, sequence: int) -> str:
    """Generate a new patient number."""
    return f"P-{year}-{sequence:06d}"


def validate_email(email: Optional[str]) -> bool:
    """Basic email validation."""
    if not email:
        return True
    return bool(re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email))
