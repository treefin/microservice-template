#!/bin/sh

set -euo pipefail

host="$1"
password="$2"
shift 2

until PGPASSWORD="$password" psql -h "$host" -U "postgres" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"
exec "$@"