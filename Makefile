RUN = docker exec app poetry run 

build:
	docker compose --env-file ./env/.env.dev -f docker-compose.dev.yaml build

run:
	docker compose --env-file ./env/.env.dev -f docker-compose.dev.yaml up -d

restart:
	docker restart $$(docker ps -a -q)

migrations:
	$(RUN) python3 ./src/manage.py makemigrations

migrate:
	$(RUN) python3 ./src/manage.py migrate

stop:
	docker stop $$(docker ps -a -q)

delete:
	docker rm $$(docker ps -a -q)

rebuld:
	make build
	make run

logs:
	docker logs app -f

set_langueage:
	$(RUN) django-admin makemessages -l $(flag)

compile_language:
	$(RUN) django-admin compilemessages -l $(flag)

requrements_install:
	$(RUN) poetry install