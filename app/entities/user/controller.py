from datetime import datetime, timezone, timedelta
from typing import Annotated

from fastapi import Depends
from jose import jwt, JWTError

from app.config import ACCESS_TOKEN_EXPIRE_DAYS, settings, ALGORITHM
from app.controllers.exceptions import NotFound, AlreadyExists
from app.database import SessionLocal
from app.security import verify_password, oauth2_scheme, get_password_hash
from . import models, schemas


class CredentialsException(Exception):
    """"""


class User:
    model = models.User
    db = SessionLocal()
    datetime_format = "%Y-%m-%d %H:%M:%S"

    def __init__(self, id_got: int):
        user = self.db.query(self.model).filter(self.model.id == id_got).first()
        if not user:
            raise NotFound()

        self.db_entity: models.User = user

    @classmethod
    def from_phone(cls, phone: str) -> 'User':
        print(phone)
        user = cls.db.query(cls.model).filter(models.User.phone == phone).first()
        print(user)
        if not user:
            raise NotFound()

        return cls(id_got=user.id)

    def verify_password(self, password: str) -> bool:
        return verify_password(password, self.db_entity.password_hash)

    def create_access_token(self) -> str:
        self._update()

        data = {"phone": self.db_entity.phone, "id": self.db_entity.id}
        expires = datetime.now(timezone.utc) + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)

        data["expires_str"] = expires.strftime(self.datetime_format)
        encoded_jwt = jwt.encode(data, settings.secret_key, algorithm=ALGORITHM)
        return encoded_jwt

    @classmethod
    async def get_current_user(cls, token: Annotated[str, Depends(oauth2_scheme)]) -> 'User':

        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
            user_id: int = payload.get("id")
            if user_id is None:
                raise CredentialsException

            expires_str: str = payload.get("expires_str")
            expires = datetime.strptime(expires_str, cls.datetime_format).replace(tzinfo=timezone.utc)
            if datetime.now(timezone.utc) > expires:
                raise CredentialsException

        except JWTError:
            raise CredentialsException

        return cls(id_got=user_id)

    def _update(self):
        self.db.refresh(self.db_entity)

    @property
    def schema(self) -> schemas.UserReturn:
        self._update()

        return schemas.UserReturn(**self.db_entity.__dict__, avatar=None)

    @classmethod
    def create(cls, schema: schemas.UserCreate) -> 'User':
        user = cls.db.query(cls.model).filter(models.User.phone == schema.phone).first()
        if user:
            raise AlreadyExists()

        # TODO avatar
        password_hash = get_password_hash(schema.password)

        db_user = cls.model(
            **schema.dict(exclude={'password', 'avatar'}),
            avatar_path=None,
            password_hash=password_hash
        )

        cls.db.add(db_user)
        cls.db.commit()
        cls.db.refresh(db_user)
        return cls(db_user.id)

    def update(self, schema: schemas.UserUpdate):
        self.db_entity.update(schema.dict(exclude={'avatar'}), avatar_path=None)
        self.db.commit()
        self._update()
        