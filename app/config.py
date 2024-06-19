from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://fastapi_traefik:fastapi_traefik@localhost:5432/fastapi_traefik"
    secret_key: str
    suggest_key: str
    geo_code_key: str


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 1
IMAGES_FOLDER = "images/"
settings = Settings()
