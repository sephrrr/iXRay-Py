"""Exceptions raised by ixraypy."""

from __future__ import annotations

from typing import Any


class IXRayError(Exception):
    """Base class for every error raised by this library."""


class TransportError(IXRayError):
    """The panel could not be reached (DNS, connection, timeout)."""


class APIError(IXRayError):
    """The panel answered with an error status.

    Attributes:
        status_code: HTTP status returned by the panel.
        detail: Parsed ``detail`` field of the error body, or the raw text.
        body: The full decoded body when it was JSON.
    """

    def __init__(self, status_code: int, detail: Any, body: Any = None) -> None:
        self.status_code = status_code
        self.detail = detail
        self.body = body
        super().__init__(f"HTTP {status_code}: {detail}")


class AuthenticationError(APIError):
    """401: missing, invalid or expired credentials."""


class OTPRequiredError(AuthenticationError):
    """401 with ``otp_required``: the admin has two-factor enabled; pass ``otp``."""


class PermissionDeniedError(APIError):
    """403: the credentials lack the permission for this call."""


class NotFoundError(APIError):
    """404: the object does not exist (or is outside your scope)."""


class ConflictError(APIError):
    """409: a unique field clashes with an existing object."""


class ValidationError(APIError):
    """422: the payload failed validation; see ``detail`` for the fields."""


class RateLimitedError(APIError):
    """429: too many requests; back off and retry."""


class ServerError(APIError):
    """5xx: the panel failed internally."""


_BY_STATUS: dict[int, type[APIError]] = {
    401: AuthenticationError,
    403: PermissionDeniedError,
    404: NotFoundError,
    409: ConflictError,
    422: ValidationError,
    429: RateLimitedError,
}


def error_for(status_code: int, detail: Any, body: Any = None) -> APIError:
    """Pick the exception class for a status code."""
    if status_code == 401 and detail == "otp_required":
        return OTPRequiredError(status_code, detail, body)
    cls = _BY_STATUS.get(status_code)
    if cls is None:
        cls = ServerError if status_code >= 500 else APIError
    return cls(status_code, detail, body)
