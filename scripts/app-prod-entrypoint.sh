#!/bin/sh

poetry run python3 src/manage.py migrate
poetry run gunicorn src.settings.wsgi --bind 0.0.0.0:8000 --log-level debug 