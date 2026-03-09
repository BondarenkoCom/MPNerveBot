from __future__ import annotations

from bot.services.validation import ValidationResult


class MarketplaceBApiClient:
    async def validate_credentials(self, access_token: str) -> ValidationResult:
        if len(access_token.strip()) < 6:
            return ValidationResult(
                is_valid=False,
                account_name=None,
                error_text="Marketplace B rejected the provided access token.",
            )

        return ValidationResult(
            is_valid=True,
            account_name="Marketplace B account",
            error_text=None,
        )
