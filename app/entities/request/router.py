import random
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .crud import RequestCRUD
from .schemas import RequestReturn, RequestCreate, RequestGot
from ..user.controller import User
from ...dependencies import get_db

request_router = APIRouter(
    prefix="/requests",
    tags=["requests"]
)


@request_router.post("/me", response_model=RequestReturn)
def create_request(req: RequestGot,
                   current_user: Annotated[User, Depends(User.get_current_user)],
                   db: Session = Depends(get_db) ):
    cost = random.randint(100, 1000)
    try:
        new_request = RequestCRUD(db).create(RequestCreate(**req.dict(), user_id=current_user.schema.id, cost=cost))
        return new_request
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))


@request_router.put("/{request_id}", response_model=RequestReturn)
def update_request_status(request_id: int,
                          new_status: str,
                          current_user: Annotated[User, Depends(User.get_current_user)],
                          db: Session = Depends(get_db) ):
    try:
        updated_request = RequestCRUD(db).update_request_status(request_id, new_status, current_user.schema.id)
        if not updated_request:
            raise HTTPException(status_code=404, detail="Request not found")
        return updated_request
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))


@request_router.get("/me", response_model=list[RequestReturn])
async def get_my_cars(current_user: Annotated[User, Depends(User.get_current_user)],
                      db: Session = Depends(get_db)) -> list[RequestReturn]:
    return RequestCRUD(db).get_requests_by_user_id(current_user.schema.id)


@request_router.get("/user/{user_id}", response_model=list[RequestReturn])
async def get_for_user(user_id: int, db: Session = Depends(get_db)):
    return RequestCRUD(db).get_requests_by_user_id(user_id)


