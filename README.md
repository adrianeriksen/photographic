# Photographic

I like square photos. Unquestionably a hobby project.

## Requirements

PostgresSQL should be used as a database.

## Configuring the environment

The following environment variables should be set before running:

```
SECRET_KEY
DB_NAME
DB_USER
DB_PASSWORD
DB_HOST
DB_PORT
```

In production, the following should also be set:

```
MEDIA_ROOT
MEDIA_URL
STATIC_ROOT
STATIC_URL
```

During development, a `.env` file can be used to declare the environment variables. Pipenv will parse and load the file.

## Tricks

During development, a Postgres database can be spun up with the following command:

```
$ docker run --name postgres-db -e POSTGRES_PASSWORD=[Very good password] -p 5432:5432 -d postgres
```

## Credits

Favicon graphics created by Twitter licensed under CC-BY 4.0.
https://github.com/twitter/twemoji