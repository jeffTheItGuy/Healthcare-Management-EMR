"""Input validators for Zimbabwe-specific fields."""
import re
from typing import Optional


def validate_zimbabwe_national_id(national_id: str) -> bool:
    """
    Validate Zimbabwe National ID format.
    Format: XX-XXXXXX-X-XX  (e.g., 63-1234567-A-12)
    Where:
      - First 2 digits: district code
      - Next 6-7 digits: serial number
      - Letter: checksum/series
      - Last 2 digits: sequence
    """
    if not national_id:
        return True  # Optional field
    
    pattern = r"^\d{2}-\d{6,7}-[A-Z]-\d{2}$"
    return bool(re.match(pattern, national_id.strip().upper()))


def validate_phone_zw(phone: Optional[str]) -> bool:
    """
    Validate Zimbabwe phone number.
    Accepts:
      - Local format: 077xxxxxxx, 071xxxxxxx, 073xxxxxxx
      - International: +26377xxxxxxx
      - Ecocash/Zipit often use: 07xxxxxxxx
    """
    if not phone:
        return True  # Optional field
    
    cleaned = phone.strip().replace(" ", "").replace("-", "")
    
    # International +263...
    if cleaned.startswith("+263"):
        return len(cleaned) == 12 and cleaned[4:].isdigit()
    
    # Local 07...
    if cleaned.startswith("07") or cleaned.startswith("08"):
        return len(cleaned) == 10 and cleaned.isdigit()
    
    # Landline (optional support)
    if cleaned.startswith("0"):
        return len(cleaned) >= 9 and cleaned.isdigit()
    
    return False


def validate_patient_number(patient_number: str) -> bool:
    """Validate patient number format: P-YYYY-NNNNNN"""
    if not patient_number:
        return False
    pattern = r"^P-\d{4}-\d{6}$"
    return bool(re.match(pattern, patient_number.strip().upper()))


def generate_patient_number(year: int, sequence: int) -> str:
    """Generate a new patient number."""
    return f"P-{year}-{sequence:06d}"


def validate_email(email: Optional[str]) -> bool:
    """Basic email validation."""
    if not email:
        return True
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))