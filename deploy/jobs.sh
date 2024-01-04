rm docker-compose.dev.yaml
mv docker-compose.prod.yaml docker-compose.yaml
mv ./deploy/init-letsencrypt.sh init-letsencrypt.sh
rm Makefile