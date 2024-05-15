import random
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from .crud import RequestCRUD
from .schemas import RequestReturn, RequestCreate, RequestGot
from ..user.controller import User

request_router = APIRouter(
    prefix="/requests",
    tags=["requests"]
)


@request_router.post("/me", response_model=RequestReturn)
def create_request(req: RequestGot, current_user: Annotated[User, Depends(User.get_current_user)]):
    cost = random.randint(100, 1000)
    try:
        new_request = RequestCRUD().create(RequestCreate(**req.dict(), user_id=current_user.schema.id, cost=cost))
        return new_request
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))


@request_router.put("/{request_id}", response_model=RequestReturn)
def update_request_status(request_id: int, new_status: str):
    try:
        updated_request = RequestCRUD().update_request_status(request_id, new_status)
        if not updated_request:
            raise HTTPException(status_code=404, detail="Request not found")
        return updated_request
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))


@request_router.get("/me", response_model=RequestReturn)
def create_request(req: RequestCreate):
    try:
        new_request = RequestCRUD().create(req)
        return new_request
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))