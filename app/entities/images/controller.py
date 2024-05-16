from PIL import UnidentifiedImageError

from app.database import SessionLocal
from app.entities.images import models
from app.entities.images.image_worker import convert_base64_to_image, resize_image, save_image, open_image, \
    encode_image_to_base64, check_and_convert_to_jpg


class ImageError(Exception):
    """"""


class ImageNotFound(Exception):
    """"""


class Image:
    model = models.Image
    dir = "images/"

    @classmethod
    def add_image(cls, base64_file: str, db: SessionLocal) -> int:
        """
        Метод для добавления картинки
        :param base64_file: jpg файл в кодировки base64
        :return: картинка
        """

        # TODO check format
        try:
            img = convert_base64_to_image(base64_file)
        except UnidentifiedImageError:
            raise ImageError
        img = check_and_convert_to_jpg(img)
        img = resize_image(img)

        db_img = cls.model(filename="Not impl")
        db.add(db_img)
        db.commit()
        db.refresh(db_img)

        save_image(img, db_img.id)

        return db_img.id

        # check size
        # reformat
        # generate uuid and save
        # push in db

    @classmethod
    def get_image(cls, img_id: int, size_type: int) -> str:
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

