#!/bin/bash

# База не успевает подняться
sleep 10


python manage.py migrate
python manage.py collectstatic --no-input
python manage.py load_ingredients
python manage.py load_tags


gunicorn --bind 0.0.0.0:8080 foodgram.wsgi
