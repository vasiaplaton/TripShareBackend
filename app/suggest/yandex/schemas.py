from typing import Optional

from pydantic import BaseModel


class YandexTextH1(BaseModel):
    begin: int
    end: int


class YandexText(BaseModel):
    text: str
    hl: Optional[list[YandexTextH1]] = None


class Distance(BaseModel):
    value: float
    text: str


class SuggestResult(BaseModel):
    title: YandexText
    subtitle: Optional[YandexText] = None
    tags: list[str]
    distance: Distance
    uri: str


class SuggestResults(BaseModel):
    suggest_reqid: str
    results: list[SuggestResult]
