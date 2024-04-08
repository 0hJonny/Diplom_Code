#!/bin/bash

# Check if the user is root
if [[ $EUID -eq 0 ]]; then
    SUDO=""
else
    SUDO="sudo"
fi

# Check the operating system
if [[ "$(uname)" == "Linux" ]]; then
    # Install docker-compose if not already installed
    if ! command -v docker-compose &> /dev/null; then
        echo "Installing docker-compose..."
        $SUDO apt-get update
        $SUDO apt-get install -y docker-compose
    fi
fi

# Create necessary directories
$SUDO mkdir -p /opt/postgres/backup /opt/redis /opt/redis/redis.conf /opt/exchange /opt/postgres/pgadmin /opt/minio/data

# Set permissions for directories
$SUDO chown 1001:1001 -R /opt/minio/data/ /opt/exchange/

# Set access permissions
$SUDO chown -R 5050:5050 /opt/postgres/pgadmin/

# Start Docker Compose
cd docker
docker-compose up --build
