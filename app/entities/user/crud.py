from datetime import datetime, timezone, timedelta
from typing import Annotated, Optional

from fastapi import Depends
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.database import models
from app.database.database import SessionLocal
from app.dependencies import get_db
from app.entities.car.crud import CarCrud
from app.entities.car import crud as car_crud
from app.entities.exceptions import AlreadyExists, NotFound
from app.entities.user import schemas
from app.entities.user.security import oauth2_scheme, get_password_hash
from app.config import settings, ALGORITHM, ACCESS_TOKEN_EXPIRE_DAYS

datetime_format = "%Y-%m-%d %H:%M:%S"


def _model_to_schema(db_item: models.User, db: SessionLocal, car_dto: bool = True) -> Optional[schemas.UserReturn]:
    if db_item is None:
        return None
    d = db_item.__dict__
    if car_dto:
        d["cars"] = car_crud._models_to_schema(CarCrud(db).get_by_user_id(db_item.id))
    return schemas.UserReturn.model_validate(db_item.__dict__)


def _models_to_schema(db_items: list[models.User], db: SessionLocal) -> list[schemas.UserReturn]:
    return [_model_to_schema(db_item, db) for db_item in db_items]


class UserCrud:
    def __init__(self, db: SessionLocal):
        self.db = db

    def create(self, schema: schemas.UserCreate, commit: bool = True) -> models.User:
        user = self.db.query(models.User).filter(models.User.phone == schema.phone).first()
        if user:
            raise AlreadyExists

        password_hash = get_password_hash(schema.password)

        db_user = models.User(
            **schema.dict(exclude={'password'}),
            password_hash=password_hash
        )

        self.db.add(db_user)
        if commit:
            self.db.commit()
        else:
            self.db.flush()

        self.db.refresh(db_user)

        return db_user

    def update_rating(self, user_id: int, rating: float, commit: bool = True):
        db_user = self.get_user_by_id(user_id)
        db_user.rating = rating

        if commit:
            self.db.commit()
        else:
            self.db.flush()

        self.db.refresh(db_user)

        return db_user

    def update(self, user_id: int, user: schemas.UserUpdate, commit: bool = True):
        item = self.db.query(models.User).filter(models.User.id == user_id).first()
        if item is None:
            raise NotFound

        item.update(**user.model_dump())
        if commit:
            self.db.commit()
        else:
            self.db.flush()

        self.db.refresh(item)
        return item

    def get_user_by_phone(self, phone: str):
        user = self.db.query(models.User).filter(models.User.phone == phone).first()
        return user

    def get_user_by_id(self, id: int):
        user = self.db.query(models.User).filter(models.User.id == id).first()
        return user


class CredentialsException(Exception):
    """"""


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],
                           db: Session = Depends(get_db)) -> schemas.UserReturn:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
        user_id: int = payload.get("id")
        if user_id is None:
            raise CredentialsException

        expires_str: str = payload.get("expires_str")
        expires = datetime.strptime(expires_str, datetime_format).replace(tzinfo=timezone.utc)
        if datetime.now(timezone.utc) > expires:
            raise CredentialsException

    except JWTError:
        raise CredentialsException

    return _model_to_schema(UserCrud(db).get_user_by_id(user_id), db)


def create_access_token(user: models.User) -> str:
    data = {"phone": user.phone, "id": user.id}
    expires = datetime.now(timezone.utc) + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)

    data["expires_str"] = expires.strftime(datetime_format)
    encoded_jwt = jwt.encode(data, settings.secret_key, algorithm=ALGORITHM)
    return encoded_jwt
