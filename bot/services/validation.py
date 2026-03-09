from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ValidationResult:
    is_valid: bool
    account_name: str | None
    error_text: str | None
