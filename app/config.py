from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://fastapi_traefik:fastapi_traefik@localhost:5432/fastapi_traefik"


settings = Settings()
