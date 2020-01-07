FROM python:3.7.5-alpine
RUN apk add make build-base python3-dev libc-dev libffi-dev libressl-dev openssl-dev linux-headers curl git
RUN pip install --upgrade pip
RUN pip install poetry
RUN mkdir -p /build
WORKDIR /build
COPY pyproject.toml .
COPY poetry.lock .
COPY poetry.toml .
RUN poetry env use python
RUN poetry install