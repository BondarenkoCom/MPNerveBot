from __future__ import annotations

from bot.services.validation import ValidationResult


class MarketplaceAApiClient:
    async def validate_credentials(self, account_id: str, access_key: str) -> ValidationResult:
        if len(account_id.strip()) < 3 or len(access_key.strip()) < 6:
            return ValidationResult(
                is_valid=False,
                account_name=None,
                error_text="Marketplace A rejected the provided credentials.",
            )

        return ValidationResult(
            is_valid=True,
            account_name="Marketplace A account",
            error_text=None,
        )
