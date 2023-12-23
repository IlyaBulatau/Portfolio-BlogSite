#!/bin/sh
export MODE='prod'
export $(grep -v '^#' ./env/.env.dev | xargs)

poetry run python3 src/manage.py runserver 0.0.0.0:8000