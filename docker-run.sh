#!/bin/sh

python manage.py makemigrations
python manage.py migrate

exec gunicorn order_management.wsgi:application --bind 0.0.0.0:8000
