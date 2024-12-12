@echo off
cd ..\docker
echo Directory: %cd%
echo Running Docker Compose Up...
docker-compose up -d
cd ..\scripts