```commandline
export DATABASE_URL=postgresql://fastapi_traefik:fastapi_traefik@localhost:5432/fastapi_traefik && export SECRET_KEY="" && export SUGGEST_KEY="" && export GEO_CODE_KEY="" 
alembic revision --autogenerate -m "init" 
alembic upgrade head

```
