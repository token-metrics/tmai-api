"""Custom exceptions used throughout the Token Metrics SDK."""

from __future__ import annotations

from typing import Any, Dict, Optional


class MissingAPIKeyError(ValueError):
    """Raised when the API key is missing from configuration."""


class APIRequestError(Exception):
    """Represents an error returned by the Token Metrics API."""

    def __init__(
        self,
        *,
        endpoint: str,
        method: str,
        params: Optional[Dict[str, Any]] = None,
        status_code: Optional[int] = None,
    ) -> None:
        self.endpoint = endpoint
        self.method = method
        self.params = params or {}
        self.status_code = status_code
        super().__init__(self.__str__())

    def __str__(self) -> str:
        status = f" status={self.status_code}" if self.status_code is not None else ""
        return (
            f"API request failed:{status} method={self.method} endpoint={self.endpoint} "
            f"params={self.params}"
        )
