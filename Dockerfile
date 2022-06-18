FROM python:3.10-slim

WORKDIR /usr/bin/photographic

RUN pip install --upgrade pip
RUN pip install pipenv

COPY Pipfile Pipfile.lock ./
RUN pipenv install --deploy

RUN mkdir -p /var/photographic/media
RUN mkdir -p /var/photographic/static

COPY . .
