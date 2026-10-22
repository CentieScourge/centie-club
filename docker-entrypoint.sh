#!/bin/sh
# Entrypoint: wait for PostgreSQL, apply migrations, collect static files, then run CMD
set -e

DB_HOST="${DB_HOST:-db}"
DB_PORT="${DB_PORT:-5432}"

echo "Waiting for PostgreSQL at ${DB_HOST}:${DB_PORT}..."
until nc -z "$DB_HOST" "$DB_PORT"; do
  sleep 1
done
echo "PostgreSQL is up."

python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec "$@"
