from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.entities.chats import schemas, chat_crud, message_crud
from app.entities.chats.chat_crud import ChatCrud
from app.entities.chats.message_crud import ChatMessageCrud
from app.entities.chats.schemas import ChatMessageCreate
from app.entities.user.crud import get_current_user
from app.entities.user.schemas import UserReturn

chat_router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)


@chat_router.get("/me", response_model=list[schemas.ChatReturn])
async def get_my_chats(current_user: Annotated[UserReturn, Depends(get_current_user)],
                       db: Session = Depends(get_db)):
    chats = ChatCrud(db).get_chats_by_user_id(current_user.id)
    return chat_crud._models_to_schema(chats, db)


@chat_router.post("/messages", response_model=schemas.ChatMessageReturn)
async def create_message(message: ChatMessageCreate,
                         current_user: Annotated[UserReturn, Depends(get_current_user)],
                         db: Session = Depends(get_db)):
    return message_crud._model_to_schema(ChatMessageCrud(db).send_message(message, current_user.id))


@chat_router.get("/{chat_id}/messages", response_model=list[schemas.ChatMessageReturn])
async def get_messages_by_chat_id(chat_id: int, db: Session = Depends(get_db)):
    return message_crud._models_to_schema(ChatMessageCrud(db).get_message_by_chat_id(chat_id))