# My_journey project

## Before start up

For start up application you should have:

- [python>=3.12](https://www.python.org/downloads/)
- [pdm](https://pdm-project.org/latest/)
- [docker](https://www.docker.com/products/docker-desktop/)

## Dependencies

Description of all variables

[environments.md](https://github.com/DzmitryZhybryk/base_fastapi_project/blob/main/docs/environments.md?plain=1)

### install base dependencies

Dependencies installation guide

[pdm.md](https://github.com/DzmitryZhybryk/base_fastapi_project/blob/main/docs/pdm.md?plain=1)

## Work with linter

Linter guide

[ruff.md](https://github.com/DzmitryZhybryk/base_fastapi_project/blob/main/docs/ruff.md?plain=1)

## Work with type analyzer

[mypy.md](https://github.com/DzmitryZhybryk/base_fastapi_project/blob/main/docs/mypy.md?plain=1)

## Migration

Create migration
```bash
docker exec -it my_helper pdm run alembic revision --autogenerate -m "init_migration" 
```

Upgrade migration
```bash
docker exec -it my_helper pdm run alembic upgrade heads
```

Downgrade migration
```bash
docker exec -it my_helper pdm run alembic downgrade $revision_name
```

## Run project in Development mode

For start project
```bash
docker compose -f ./docker-compose-dev.yaml up --build
```