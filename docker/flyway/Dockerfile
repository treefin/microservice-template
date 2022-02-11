FROM flyway/flyway:7

USER root

RUN apt-get update && apt-get install -y postgresql-client

RUN mkdir -p /flyway/bin

COPY ./wait-for-postgres.sh /flyway/bin/wait-for-postgres.sh
