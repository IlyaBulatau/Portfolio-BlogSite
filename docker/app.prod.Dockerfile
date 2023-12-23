FROM python:3.10.6-alpine

ENV PYTHONUNBUFFERED 1 \
    PYTHONDONTWRITEBYTECODE 1

ENV HOME=/home/admin/web/project

RUN apk update && \
    apk add musl-dev libpq-dev gcc gettext

WORKDIR $HOME

COPY .. .

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry install --no-root --no-directory

EXPOSE 80

RUN addgroup -S web && adduser -S admin -G web && \
    chown -R admin:web $HOME && \
    chmod 755 $HOME

USER admin

ENTRYPOINT [ "sh", "./scripts/app-prod-entrypoint.sh" ]