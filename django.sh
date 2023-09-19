#!/bin/bash

echo "create migrations"
python manage.py makemigrations demo
echo "=============================="

echo "migrating database"
python manage.py migrate
echo "=============================="

echo "start server"
python manage.py runserver 0.0.0.0:8000
echo "==========running=================="