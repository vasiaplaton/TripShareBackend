from typing import List, Optional
from pydantic import BaseModel


class ImageSchema(BaseModel):
    base64_file: str