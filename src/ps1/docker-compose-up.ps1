Write-Host "Running Docker Compose Up..."
docker compose -f ..\..\compose.yml --env-file ..\config\.env.docker up