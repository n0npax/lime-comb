FROM python:3.7.5-alpine
RUN apk add make build-base python3-dev libc-dev libffi-dev libressl-dev openssl-dev linux-headers curl git bash tree gnupg
RUN apk add --update nodejs npm
RUN npm install -g firebase-tools
RUN apk --no-cache add openjdk11 --repository=http://dl-cdn.alpinelinux.org/alpine/edge/community
RUN pip install --upgrade pip
RUN pip install poetry
RUN mkdir -p /build
WORKDIR /build
COPY pyproject.toml .
COPY poetry.lock .
COPY poetry.toml .
RUN poetry env use python3.7
RUN poetry install
