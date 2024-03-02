#!/bin/sh

echo "Apply migrations"

python3 manage.py migrate
echo "finished migrations"
python3 manage.py runserver 0.0.0.0:8000