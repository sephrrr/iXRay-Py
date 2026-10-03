"""ixraypy: async Python client for the iXRay panel API."""

__version__ = "0.1.0"

from ixraypy import models
from ixraypy.client import IXRayClient
from ixraypy.exceptions import (
    APIError,
    AuthenticationError,
    ConflictError,
    IXRayError,
    NotFoundError,
    OTPRequiredError,
    PermissionDeniedError,
    RateLimitedError,
    ServerError,
    TransportError,
    ValidationError,
)

__all__ = [
    "IXRayClient",
    "models",
    "IXRayError",
    "TransportError",
    "APIError",
    "AuthenticationError",
    "OTPRequiredError",
    "PermissionDeniedError",
    "NotFoundError",
    "ConflictError",
    "ValidationError",
    "RateLimitedError",
    "ServerError",
    "__version__",
]
