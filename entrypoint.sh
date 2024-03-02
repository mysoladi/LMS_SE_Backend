#!/bin/sh

echo "Apply migrations"

cd ./LMS_SE_Backend
python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:8000