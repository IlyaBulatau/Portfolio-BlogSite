#!/bin/sh
export MODE='prod'
export PYTHONPATH=$(pwd)/src

export $(grep -v '^#' ./env/.env.prod | xargs)

poetry run python3 src/manage.py migrate
poetry run gunicorn src.settings.wsgi --bind 0.0.0.0:8000