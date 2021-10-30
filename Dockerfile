FROM python:3.9.7-alpine3.14

RUN set -xe \
    && apk --no-cache add git less openssh gcc musl-dev libffi-dev libgit2-dev libssh2 build-base

WORKDIR /app

# Project Deps
COPY poetry.lock pyproject.toml /app/
COPY src/ /app/src/

RUN set -xe \
    && pip install --upgrade pip \
    && pip install poetry \
    && poetry config --local virtualenvs.create false \
    && poetry install


CMD ["plextools --help"]
