#!bin/sh
python manage.py makemigrations
python manage.py migrate
#python manage.py collectstatic --no-input 
#python manage.py createsuperuser --no-input
python manage.py runserver 0.0.0.0:8000 #0.0.0.0 is needed or else i wont be able to access this port via docker-localhost
