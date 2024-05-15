from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from . import schemas
from . import controller
from .crud import RequestCRUD
from .schemas import RequestReturn, RequestCreate
from ..user.controller import User

request_router = APIRouter(
    prefix="/requests",
    tags=["requests"]
)


@request_router.post("/", response_model=RequestReturn)
def create_request(req: RequestCreate):
    try:
        new_request = RequestCRUD().create(req)
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
