from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette import status

from . import schemas
from . import controller
from app.controllers.exceptions import NotFound, AlreadyExists
from app.security import Token
from ...dependencies import get_db

user_router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@user_router.post("/token")
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Session = Depends(get_db)
) -> Token:
    """Логинимся для получения токена"""
    exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        user = controller.User.from_phone(form_data.username, db)
        if not user.verify_password(form_data.password):
            raise exc
    except NotFound:
        raise exc

    token = user.create_access_token()

    return Token(access_token=token, token_type="bearer")


@user_router.post("/")
async def register_user(schema: schemas.UserCreate, db: Session = Depends(get_db)) -> schemas.UserReturn:
    """Регистрируемся"""
    try:
        return controller.User.create(schema, db).schema
    except AlreadyExists:
        raise HTTPException(status_code=400, detail="Already exisits")
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=e.detail)


@user_router.get("/me")
async def read_users_me(
        current_user: Annotated[controller.User, Depends(controller.User.get_current_user)],
) -> schemas.UserReturn:
    """Читаем свои данные"""
    return current_user.schema


@user_router.put("/me")
async def update_users_me(
        schema: schemas.UserUpdate,
        current_user: Annotated[controller.User, Depends(controller.User.get_current_user)],
        db: Session = Depends(get_db)
) -> schemas.UserReturn:
    """Обновляем свои данные"""
    return current_user.update(schema, db)


@user_router.get("/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)) -> schemas.UserReturn:
    """Читаем свои данные"""
    return controller.User(user_id, db).schema
