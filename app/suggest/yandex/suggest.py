import json

import httpx

from app.config import settings
from app.suggest.yandex.exceptions import ReqError, NotFoundError
from app.suggest.yandex.schemas import SuggestResults


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

    async def get_suggestions(self, text: str) -> SuggestResults:
        url = f"{self.url}?apikey={settings.suggest_key}&text={text}&attrs=uri"
        dd = await self.send_get(url)
        print(dd)
        return SuggestResults(**dd)