"""Custom application exceptions."""
from fastapi import HTTPException, status


class ZimEMRException(HTTPException):
    """Base exception for ZimEMR."""
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)


class AuthenticationError(ZimEMRException):
    def __init__(self, detail: str = "Authentication failed"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class AuthorizationError(ZimEMRException):
    def __init__(self, detail: str = "Not authorized to perform this action"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class ResourceNotFoundError(ZimEMRException):
    def __init__(self, resource: str = "Resource", detail: str = None):
        msg = detail or f"{resource} not found"
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=msg)


class ValidationError(ZimEMRException):
    def __init__(self, detail: str = "Validation failed"):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)


class DuplicateResourceError(ZimEMRException):
    def __init__(self, resource: str = "Resource"):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"{resource} already exists",
        )