import json

import httpx

from app.config import settings


class ADCBetError(Exception):
    """Общее исключение при ошибке c ADC Bet App"""


class ReqError(ADCBetError):
    """Исключение, выбрасываемое при ошибке в запросе"""


class NotFoundError(ReqError):
    """Не нашли что-то где-то"""


class YandexSuggest:
    def __init__(self):
        self.url = "https://suggest-maps.yandex.ru/v1/suggest"

    async def send_get(self, url):
        async with httpx.AsyncClient() as client:
            try:
                result = await client.get(url, timeout=10)
            except httpx.HTTPError as e:
                raise ReqError(e) from e

        if result.status_code not in [200, 201]:
            if result.status_code == 404:
                raise NotFoundError("Not found somewhere")
            raise ReqError(f"Got error status code, {result.status_code}")

        parsed_response = json.loads(result.text)
        return parsed_response

    def get_suggestions(self, text: str):
        url = f"{self.url}?apikey={settings.suggest_key}&text={text}&attrs=uri"
