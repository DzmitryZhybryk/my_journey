FROM python:3.12
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /code

RUN apt update

COPY ./pyproject.toml ./pdm.lock ./alembic.ini /code/

RUN pip install pdm && \
    pdm install

COPY ./migrations /code/migrations/
COPY ./app  /code/app/