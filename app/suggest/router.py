from fastapi import APIRouter

from app.suggest.yandex.geo_coder import YandexCoder
from app.suggest.yandex.schemas import SuggestResults
from app.suggest.yandex.suggest import YandexSuggest

yandex_router = APIRouter(
    prefix="/yandex",
    tags=["yandex"]
)


@yandex_router.get("/suggest/{text}", response_model=SuggestResults)
async def get_suggestion(text: str) -> SuggestResults:
    return await YandexSuggest().get_suggestions(text)


@yandex_router.get("/pos", response_model=str)
async def get_code(uri: str) -> str:
    print(uri)
    return await YandexCoder().uri_to_coords(uri)

