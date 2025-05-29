#!/bin/bash

cd /app/backend/tiny-link/
python manage.py migrate
python manage.py runserver_plus 0.0.0.0:8080 --cert-file /cert.pem --key-file /key.pem
