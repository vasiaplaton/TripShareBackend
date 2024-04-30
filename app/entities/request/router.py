from typing import Annotated

from fastapi import APIRouter, Depends

from . import schemas
from . import controller
from ..user.controller import User

request_router = APIRouter(
    prefix="/requests",
    tags=["requests"]
)


