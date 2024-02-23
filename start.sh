#!/bin/sh

cd docker

sudo mkdir -p /opt/postgres/backup /opt/redis /opt/redis/redis.conf /opt/exchange /opt/postgres/pgadmin /opt/minio

# Set permissions for directories
sudo chown 1001:1001 -R /opt/minio/data/ /opt/exchange/

# Set access permissions
sudo chown -R 5050:5050 /opt/postgres/pgadmin/

# Start Docker Compose
docker-compose up