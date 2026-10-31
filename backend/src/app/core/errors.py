"""Application error types."""

from __future__ import annotations


class DomainError(Exception):
    """Base class for errors that map to a client-visible response."""

    status_code = 400
    code = "domain_error"

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class CapabilityMissing(DomainError):
    """The character did not grant the scope a feature needs."""

    status_code = 403
    code = "capability_missing"


class EsiUnavailable(DomainError):
    """The external API is unreachable, rate limited, or out of error budget."""

    status_code = 503
    code = "esi_unavailable"
