from __future__ import annotations

import httpx

from bot.services.validation import ValidationResult


class OzonApiClient:
    base_url = "https://api-seller.ozon.ru"

    async def validate_credentials(self, client_id: str, api_key: str) -> ValidationResult:
        headers = {
            "Client-Id": client_id,
            "Api-Key": api_key,
            "Content-Type": "application/json",
        }
        payload = {
            "filter": {},
            "last_id": "",
            "limit": 1,
        }

        try:
            async with httpx.AsyncClient(base_url=self.base_url, timeout=20.0) as client:
                response = await client.post("/v2/product/list", headers=headers, json=payload)
        except httpx.HTTPError as exc:
            return ValidationResult(
                is_valid=False,
                account_name=None,
                error_text=f"Ошибка сети Ozon API: {exc}",
            )

        if response.status_code == 200:
            data = response.json()
            result = data.get("result", {})
            total = result.get("total")
            account_name = "Ozon"
            if isinstance(total, int):
                account_name = f"Ozon ({total} товаров)"
            return ValidationResult(is_valid=True, account_name=account_name, error_text=None)

        error_text = _extract_ozon_error(response)
        return ValidationResult(is_valid=False, account_name=None, error_text=error_text)


def _extract_ozon_error(response: httpx.Response) -> str:
    try:
        payload = response.json()
    except ValueError:
        return f"Ozon API вернул статус {response.status_code}"

    message = payload.get("message") or payload.get("error") or payload.get("details")
    if isinstance(message, list):
        message = "; ".join(str(item) for item in message)
    if not message:
        message = f"Ozon API вернул статус {response.status_code}"
    return str(message)
