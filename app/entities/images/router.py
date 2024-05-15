from fastapi import APIRouter, HTTPException

from app.entities.images.controller import ImageError, ImageNotFound, Image

image_router = APIRouter(
    prefix="/images",
    tags=["images"]
)


@image_router.post("/", response_model=int)
async def add_image(base64_file: str):
    try:
        image_id = Image.add_image(base64_file)
        return image_id
    except ImageError:
        raise HTTPException(status_code=400, detail="Invalid image format")


@image_router.get("/{img_id}", response_model=str)
async def get_image(img_id: int):
    try:
        image_data = Image.get_image(img_id, 0)
        return image_data
    except ImageNotFound:
        raise HTTPException(status_code=404, detail="Image not found")
