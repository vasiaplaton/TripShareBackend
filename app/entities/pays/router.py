from typing import Annotated

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.entities.pays import crud, schemas
from app.entities.pays.crud import PaysCrud
from app.entities.user.crud import get_current_user
from app.entities.user.schemas import UserReturn

pays_router = APIRouter(
    prefix="/pays",
    tags=["pays"]
)


@pays_router.get("/me")
async def get_pays_me(current_user: Annotated[UserReturn, Depends(get_current_user)],
                      db: Session = Depends(get_db) ) -> list[schemas.PayReturn]:
    """Создаем поездку"""
    return crud._models_to_schema(PaysCrud(db).get_for_me(current_user.id))


