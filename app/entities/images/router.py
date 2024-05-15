from fastapi import APIRouter, HTTPException

from app.entities.images.controller import ImageError, ImageNotFound, Image
from app.entities.images.schemas import ImageSchema

image_router = APIRouter(
    prefix="/images",
    tags=["images"]
)


@image_router.post("/", response_model=int)
async def add_image(im: ImageSchema):
    try:
        image_id = Image.add_image(im.base64_file)
        return image_id
    except ImageError:
        raise HTTPException(status_code=400, detail="Invalid image format")


@image_router.get("/{img_id}", response_model=ImageSchema)
async def get_image(img_id: int):
    try:
        image_data = Image.get_image(img_id, 0)
        return ImageSchema(base64_file=image_data)
    except ImageNotFound:
        raise HTTPException(status_code=404, detail="Image not found")
