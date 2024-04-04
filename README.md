# Bookstore

This is a bookstore application built with FastAPI and PostgreSQL.

## Prerequisites

- Docker
- Docker Compose

## Build and start

```bash
uvicorn app.main:app --reload
```

- Starts app for local development
- Requires DB to be running

#### Run app in docker

```bash
./run.sh local
```

- It will start both API and Database

#### Stop and remove all containers

```bash
./run.sh clean
```

#### Start only DB

```bash
./run.sh db
```

- Builds and starts DB for local development

#### Run tests

```bash
./run.sh test
```
