#!/bin/sh


echo "Waiting for PostgreSQL..."
while ! pg_isready -h db -U postgres; do
  sleep 1
done
echo "PostgreSQL is up!"


echo "Applying database migrations..."
python manage.py migrate


echo "Collecting static files..."
python manage.py collectstatic --noinput


echo "Starting server..."
gunicorn --bind 0.0.0.0:8000 skygate_airport_api.wsgi:application 
