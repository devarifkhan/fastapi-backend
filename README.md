# fastapi-backend

A FastAPI backend with async PostgreSQL via SQLModel.

## Run Postgres with Docker

```bash
docker run -d --name postgres -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=fastapi_db -p 5432:5432 postgres:16
```

API docs available at `http://localhost:8000/scalar`
