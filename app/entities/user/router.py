from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette import status

from app.database import models
from app.dependencies import get_db
from app.entities.exceptions import AlreadyExists
from app.entities.user import schemas
from app.entities.user.crud import UserCrud, _model_to_schema, get_current_user, create_access_token
from app.entities.user.security import Token, verify_password

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
    user = UserCrud(db).get_user_by_phone(form_data.username)
    if not user:
        raise exc

    if not verify_password(form_data.password, user.password_hash):
        raise exc

    token = create_access_token(user)

    return Token(access_token=token, token_type="bearer")


@user_router.post("/")
async def register_user(schema: schemas.UserCreate, db: Session = Depends(get_db)) -> schemas.UserReturn:
    """Регистрируемся"""
    try:
        return _model_to_schema(UserCrud(db).create(schema), db)
    except AlreadyExists:
        raise HTTPException(status_code=400, detail="Already exisits")
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=e.detail)


@user_router.get("/me")
async def read_users_me(
        current_user: Annotated[schemas.UserReturn, Depends(get_current_user)],
) -> schemas.UserReturn:
    """Читаем свои данные"""
    return current_user


@user_router.post("/me")
async def update_users_me(
        schema: schemas.UserUpdate,
        current_user: Annotated[schemas.UserReturn, Depends(get_current_user)],
        db: Session = Depends(get_db)
) -> schemas.UserReturn:
    """Обновляем свои данные"""
    return _model_to_schema(UserCrud(db).update(current_user.id, schema), db)


@user_router.get("/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)) -> schemas.UserReturn:
    """Читаем свои данные"""
    return _model_to_schema(UserCrud(db).get_user_by_id(user_id), db)



