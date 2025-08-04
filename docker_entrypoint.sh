#!bin/sh
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --no-input 
gunicorn setup.wsgi:application --bind 0.0.0.0:8000 #0.0.0.0 is needed or else i wont be able to access this port via docker-localhost
