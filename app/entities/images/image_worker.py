import base64
import io
import os

from PIL import Image

from app.config import IMAGES_FOLDER


def convert_base64_to_image(base64_string):
    # Decode base64 string to bytes
    image_data = base64.b64decode(base64_string)

    # Convert bytes to PIL Image
    img = Image.open(io.BytesIO(image_data))
    return img


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


def save_image(img: Image, filename):
    img.save(os.path.join(IMAGES_FOLDER, filename))


def open_image(filename):
    with open(os.path.join(IMAGES_FOLDER, filename), "rb") as f:
        image_data = f.read()
    return image_data


def encode_image_to_base64(image_data):
    base64_encoded = base64.b64encode(image_data).decode("utf-8")
    return base64_encoded