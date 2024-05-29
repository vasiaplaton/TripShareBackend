import io
import os.path

from PIL import UnidentifiedImageError, Image

from app.database import SessionLocal
from app.entities.images import models
from app.entities.images.crud import resize_image, save_image, check_and_convert_to_jpg, id_to_path


class ImageError(Exception):
    """"""


class ImageNotFound(Exception):
    """"""


class ImageCrud:
    model = models.Image
    dir = "images/"

    def __init__(self, db: SessionLocal):
        self.db = db

    def add_image(self, image_data: bytes) -> int:
        """
        Метод для добавления картинки
        :param image_data: jpg файл
        :return: картинка
        """
        try:
            img = Image.open(io.BytesIO(image_data))
        except UnidentifiedImageError:
            raise ImageError
        img = check_and_convert_to_jpg(img)

        db_img = self.model(filename="Not impl")
        self.db.add(db_img)
        self.db.commit()
        self.db.refresh(db_img)

        img = resize_image(img, max_dimension=1000)
        save_image(img, 0, db_img.id)
        img = resize_image(img, max_dimension=500)
        save_image(img, 1, db_img.id)
        img = resize_image(img, max_dimension=100)
        save_image(img, 2, db_img.id)

        return db_img.id

        # check size
        # reformat
        # generate uuid and save
        # push in db

    def get_image_path(self, img_id: int, size_type: int = 0) -> str:
        """
        Метод по получению картинки
        :param img_id:
        :param size_type:
        :return:
        """
        path = id_to_path(img_id, size_type)
        if not os.path.exists(path):
            raise ImageNotFound
        return path
