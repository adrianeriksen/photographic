FROM python:3.11-slim

WORKDIR /usr/bin/photographic

RUN pip install --upgrade pip
RUN pip install pipenv

COPY Pipfile Pipfile.lock ./
RUN pipenv install --deploy

RUN mkdir -p /var/photographic/media
RUN mkdir -p /var/photographic/static

COPY . .

ENTRYPOINT ["/usr/bin/photographic/docker-entrypoint"]
EXPOSE 8000
