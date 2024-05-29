import base64
import io
import os

from PIL import Image

from app.config import IMAGES_FOLDER


def id_to_path(idd: int, additional=""):
    return os.path.join(IMAGES_FOLDER, str(idd) + str(additional) + ".jpg")


def check_and_convert_to_jpg(img: Image):
    # Convert to JPEG if not already in JPEG format
    if img.format != 'JPEG':
        img = img.convert('RGB')
    return img


def resize_image(img: Image, max_dimension=512):
    # Resize while maintaining aspect ratio
    width, height = img.size
    if width > max_dimension or height > max_dimension:
        if width > height:
            new_width = max_dimension
            new_height = int(height * (max_dimension / width))
        else:
            new_height = max_dimension
            new_width = int(width * (max_dimension / height))
        img = img.resize((new_width, new_height))
    return img


def save_image(img: Image, additional, idd: int):
    img.save(id_to_path(idd, additional))
