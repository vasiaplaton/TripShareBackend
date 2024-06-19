from io import StringIO
from typing import Optional

import pandas as pd
from fastapi import APIRouter, UploadFile, File, Depends

from app.database import models
from app.dependencies import get_db
from app.entities.places.crud import PlacesCrud, _models_to_schema
from app.entities.places.schemas import PlaceCreate, PlaceReturn

places_router = APIRouter(
    prefix="/places",
    tags=["places"]
)


@places_router.post("/all")
async def create_epic_requests(file: UploadFile = File(...), db=Depends(get_db)):
    content = await file.read()
    # Преобразование содержимого в строку
    content_str = content.decode("utf-8")
    # Использование StringIO для создания DataFrame
    df = pd.read_csv(StringIO(content_str), delimiter=",")
    dd = df.to_dict(orient='records')
    for d in dd:
        print(d)
        p = PlaceCreate(**d,
                        address=f"{d['region']}, {d['municipality']}, {d['type']} {d['settlement']}")

        db_entity = models.Place(
            **p.dict(),
        )

        db.add(db_entity)

    db.commit()


@places_router.get("/suggest/{to_find}", response_model=list[PlaceReturn])
async def get_suggest(to_find: str, amount: Optional[int] = 100, db=Depends(get_db)):
    return PlacesCrud(db).suggest(to_find, amount)


@places_router.get("/{id}", response_model=PlaceReturn)
async def get_suggest(id: int, db=Depends(get_db)):
    return PlacesCrud(db).get_by_id(id)

