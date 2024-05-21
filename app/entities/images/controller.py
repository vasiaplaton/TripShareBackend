from PIL import UnidentifiedImageError

from app.database import SessionLocal
from app.entities.images import models
from app.entities.images.image_worker import convert_base64_to_image, resize_image, save_image, open_image, \
    encode_image_to_base64, check_and_convert_to_jpg


class ImageError(Exception):
    """"""


class ImageNotFound(Exception):
    """"""


class ImageController:
    model = models.Image
    dir = "images/"

    def __init__(self, db: SessionLocal):
        self.db = db

    def add_image(self, base64_file: str) -> int:
        """
        Метод для добавления картинки
        :param base64_file: jpg файл в кодировки base64
        :return: картинка
        """
        try:
            img = convert_base64_to_image(base64_file)
        except UnidentifiedImageError:
            raise ImageError
        img = check_and_convert_to_jpg(img)
        img = resize_image(img)

        db_img = self.model(filename="Not impl")
        self.db.add(db_img)
        self.db.commit()
        self.db.refresh(db_img)

        save_image(img, db_img.id)

        return db_img.id

        # check size
        # reformat
        # generate uuid and save
        # push in db

    def get_image(self, img_id: int, size_type: int) -> str:
        """
        Метод по получению картинки
        :param img_id:
        :param size_type:
        :return:
        """
        try:
            img = open_image(img_id)
        except OSError:
            raise ImageNotFound

        return encode_image_to_base64(img)
