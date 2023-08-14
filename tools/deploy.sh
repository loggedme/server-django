#!/bin/bash

REPOSITORY_DIRECTORY=$(dirname "$(dirname "$0")")

cd $REPOSITORY_DIRECTORY
git fetch
git checkout origin/master
pip install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py test
python3 manage.py runserver 0:80
