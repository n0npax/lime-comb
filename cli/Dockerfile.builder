FROM ubuntu:20.04
LABEL maintainer="marcin.niemira@gmail.com"
RUN apt-get update && apt-get install -y locales apt-utils && rm -rf /var/lib/apt/lists/* \
    && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
ENV LANG en_US.utf8
RUN apt-get update && apt-get install -y make python3-dev linux-libc-dev libffi-dev openssl curl git bash tree gnupg nodejs npm python3-pip python3-venv sudo openjdk-14-jdk && rm -rf /var/lib/apt/lists/*
RUN curl -sL https://firebase.tools | bash
RUN pip3 install --upgrade pip
RUN pip3 install poetry
RUN mkdir -p /build
WORKDIR /build
COPY pyproject.toml .
COPY poetry.lock .
COPY poetry.toml .
RUN poetry install
