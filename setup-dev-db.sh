#!/usr/bin/env bash

# tips:
# if you are running xxx_service locally, in .env file `POSTGRESQL_HOST=localhost`
# if you need to rebuild one of the images/services, do
# `docker-compose build <name>`
# another way to run the images/services is with --force-recreate
# `docker-compose up --force-recreate <name>`
# to watch logs, do `docker-compose logs --follow`

cp dev-only/* flyway/database-migrations/
docker rm -f xxx_service_postgres; rm -rf pgdata; docker-compose up -d xxx_service_postgres;
until docker exec xxx_service_postgres pg_isready ; do sleep 1 ; done
docker-compose up xxx_service_flyway