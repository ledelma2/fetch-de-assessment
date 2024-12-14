$kafkaNetwork = docker network ls --filter name=kafka-network --format "{{.Name}}"
if (-not $kafkaNetwork) {
    Write-Host "Network 'kafka-network' could not be found, creating network..."
    docker network create kafka-network
}