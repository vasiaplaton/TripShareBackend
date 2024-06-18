```commandline
export DATABASE_URL=postgresql://fastapi_traefik:fastapi_traefik@localhost:5432/fastapi_traefik
alembic revision --autogenerate -m "init" 
alembic upgrade head

```
