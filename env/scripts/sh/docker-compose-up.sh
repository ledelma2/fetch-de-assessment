echo "Running Docker Compose Up..."
docker compose -f ../../docker/docker-compose.networks.yml -f ../../docker/docker-compose.kafka.yml -f ../../docker/docker-compose.producer.yml up