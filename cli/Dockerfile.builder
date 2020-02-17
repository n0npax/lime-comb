FROM ubuntu:20.04
RUN apt-get update && apt-get install -y locales && rm -rf /var/lib/apt/lists/* \
    && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
ENV LANG en_US.utf8
RUN apt-get update && apt-get install -y make python3-dev linux-libc-dev libffi-dev openssl curl git bash tree gnupg nodejs npm
#&& rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install -y python3-pip python3-venv
RUN npm upgrade -g npm nodejs
RUN npm install -g firebase-tools
RUN pip3 install --upgrade pip
RUN pip3 install poetry
RUN mkdir -p /build
WORKDIR /build
COPY pyproject.toml .
COPY poetry.lock .
COPY poetry.toml .
RUN poetry env use python3
RUN poetry install
