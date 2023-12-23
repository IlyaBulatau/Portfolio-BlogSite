FROM python:3.10.6-alpine

ENV PYTHONUNBUFFERED 1 \
    PYTHONDONTWRITEBYTECODE 1

RUN apk update && \
    apk add musl-dev libpq-dev gcc gettext

WORKDIR /home/project/app

RUN mkdir /home/project/app/staticfiles

COPY . .

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry install --no-root --no-directory

RUN chmod 777 ./scripts/app-prod-entrypoint.sh

ENTRYPOINT [ "sh", "./scripts/app-prod-entrypoint.sh" ]