from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from starlette.responses import FileResponse

from app.dependencies import get_db
from app.entities.images.controller import ImageError, ImageNotFound, ImageCrud

image_router = APIRouter(
    prefix="/images",
    tags=["images"]
)


@image_router.post("/", response_model=int)
async def add_image(request: Request, db: Session = Depends(get_db)):
    try:
        image_id = ImageCrud(db).add_image(await request.body())
        return image_id
    except ImageError:
        raise HTTPException(status_code=400, detail="Invalid image format")


@image_router.get("/{img_id}")
async def get_image(img_id: int, size_type: int = 0, db: Session = Depends(get_db)):
    """
    Получаем картинку
    :param img_id: ее id
    :param size_type: тип размера - 0 большое, 1 среднее, 2 маленькое
    :param db:
    :return:
    """
    try:
        image_path = ImageCrud(db).get_image_path(img_id, size_type)
        return FileResponse(image_path)
    except ImageNotFound:
        raise HTTPException(status_code=404, detail="Image not found")
