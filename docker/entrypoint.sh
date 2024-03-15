#!/bin/bash

# Stop on error
set -e

# Optional: Wait for the database to be ready
# Useful if your Django app relies on a database like PostgreSQL, MySQL, etc.
# Example for PostgreSQL:
# while ! pg_isready -h $DB_HOST -p $DB_PORT -U $DB_USER
# do
#   echo "Waiting for postgres..."
#   sleep 2
# done

# List of required environment variables
required_env_vars=("PORT" "DJANGO_DEBUG" "DJANGO_SECRET" "DJANGO_ALLOWED_HOSTS" "CRAWLER_API_KEY")

# Check each variable
for var in "${required_env_vars[@]}"; do
    if [ -z "${!var}" ]; then
        echo "Error: Environment variable $var is not set."
        exit 1
    fi
done

echo "Entering 'crawler-action'"
cd crawler-action

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Starting Gunicorn server..."
gunicorn project.wsgi:application --bind 0.0.0.0:"$PORT"
