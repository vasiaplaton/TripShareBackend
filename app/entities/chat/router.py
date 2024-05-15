from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.entities.chat import schemas
from app.entities.chat.crud import ChatCRUD
from app.entities.chat.schemas import ChatMessage, ChatMessageCreate
from app.entities.user.controller import User

chat_router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)


@chat_router.get("/me", response_model=list[schemas.Chat])
async def get_chats_by_user_id(current_user: Annotated[User, Depends(User.get_current_user)]):
    return ChatCRUD().get_chats_by_user_id(current_user.schema.id)


@chat_router.post("/messages", response_model=ChatMessage)
async def create_message(receiver_id: int, message: ChatMessageCreate, current_user: Annotated[User, Depends(User.get_current_user)]):
    try:
        return ChatCRUD().create_message(message, current_user.schema.id, receiver_id)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))


@chat_router.get("/{chat_id}/messages", response_model=list[ChatMessage])
async def get_messages_by_chat_id(chat_id: int):
    chat_crud = ChatCRUD()
    return chat_crud.get_messages_by_chat_id(chat_id)
