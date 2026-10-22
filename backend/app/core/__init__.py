"""Core application components: security, RLS, exceptions."""
from .security import (
    verify_password,
    get_password_hash,
    create_access_token,
    decode_access_token,
    get_current_user,
    require_role,
)
from .rls import set_staff_rls_context, set_patient_rls_context
from .exceptions import (
    EMRException,
    AuthenticationError,
    AuthorizationError,
    ResourceNotFoundError,
    ValidationError,
    DuplicateResourceError,
)

__all__ = [
    "verify_password",
    "get_password_hash",
    "create_access_token",
    "decode_access_token",
    "get_current_user",
    "require_role",
    "set_staff_rls_context",
    "set_patient_rls_context",
    "EMRException",
    "AuthenticationError",
    "AuthorizationError",
    "ResourceNotFoundError",
    "ValidationError",
    "DuplicateResourceError",
]