if ! docker network ls --filter name=kafka-network --format "{{.Name}}"; then
    echo "Network 'kafka-network' could not be found, creating network..."
    docker network create kafka-network
fi