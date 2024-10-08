#!/bin/sh

# Запускаємо міграції
python manage.py migrate

# Запускаємо сервер
python manage.py runserver 0.0.0.0:8000
