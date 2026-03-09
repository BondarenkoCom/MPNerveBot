from __future__ import annotations

import httpx

from bot.services.validation import ValidationResult


class WildberriesApiClient:
    base_url = "https://common-api.wildberries.ru"

    async def validate_credentials(self, token: str) -> ValidationResult:
        headers = {
            "Authorization": token if token.lower().startswith("bearer ") else f"Bearer {token}",
        }

        try:
            async with httpx.AsyncClient(base_url=self.base_url, timeout=20.0) as client:
                response = await client.get("/api/v1/seller-info", headers=headers)
        except httpx.HTTPError as exc:
            return ValidationResult(
                is_valid=False,
                account_name=None,
                error_text=f"Ошибка сети WB API: {exc}",
            )

        if response.status_code == 200:
            data = response.json()
            name = (
                data.get("sellerName")
                or data.get("name")
                or data.get("trademark")
                or data.get("tradeMark")
                or "Wildberries"
            )
            return ValidationResult(is_valid=True, account_name=str(name), error_text=None)

        error_text = _extract_wb_error(response)
        return ValidationResult(is_valid=False, account_name=None, error_text=error_text)


def _extract_wb_error(response: httpx.Response) -> str:
    try:
        payload = response.json()
    except ValueError:
        return f"WB API вернул статус {response.status_code}"

    message = (
        payload.get("message")
        or payload.get("errorText")
        or payload.get("title")
        or payload.get("detail")
    )
    if not message:
        message = f"WB API вернул статус {response.status_code}"
    return str(message)
