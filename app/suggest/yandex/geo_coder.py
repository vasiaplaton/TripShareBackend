import json

import httpx

from app.config import settings
from app.suggest.yandex.exceptions import ReqError, NotFoundError
from app.suggest.yandex.schemas import SuggestResults, CoderResults


class YandexCoder:
    def __init__(self):
        self.url = "https://geocode-maps.yandex.ru/1.x"

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

    async def get_suggestions(self, uri: str) -> CoderResults:
        print(uri)
        url = f"{self.url}?apikey={settings.geo_code_key}&uri={uri}&format=json"
        dd = await self.send_get(url)
        print(dd)
        return CoderResults(**dd)

    async def uri_to_coords(self, uri: str):
        print(uri)
        sugg = await self.get_suggestions(uri)
        print(sugg)
        coords = sugg.response.GeoObjectCollection.featureMember
        if len(coords) == 0:
            return NotFoundError
        return coords[0].GeoObject.Point.pos
