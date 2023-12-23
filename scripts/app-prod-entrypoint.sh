#!/bin/sh
export MODE='prod'
export $(grep -v '^#' ./env/.env.dev | xargs)

poetry run gunicorn src.settings.wsgi:application --bind 0.0.0.0:8000