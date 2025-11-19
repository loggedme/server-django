#!/bin/sh

/app/manage.py migrate --no-input
/app/manage.py runserver 0.0.0.0:8000
