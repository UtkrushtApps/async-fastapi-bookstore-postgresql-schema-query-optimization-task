#!/usr/bin/env bash
set -e
cd /root/task

echo "[1/4] Starting containers with docker-compose..."
docker-compose up -d

# Wait for PostgreSQL to be ready
until docker exec bookstore-postgres pg_isready -U bookstore_user -d bookstore_db; do
    echo "Waiting for PostgreSQL to be ready..."
    sleep 1
done

sleep 2

echo "[2/4] Creating schema..."
docker exec -i bookstore-postgres psql -U bookstore_user -d bookstore_db < /root/task/schema.sql
sleep 2
echo "[3/4] Inserting sample data..."
docker exec -i bookstore-postgres psql -U bookstore_user -d bookstore_db < /root/task/data/sample_data.sql
sleep 2

echo "[4/4] Validating FastAPI..."
status=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/docs)
if [ "$status" == "200" ]; then
  echo "Setup complete: FastAPI and PostgreSQL are running."
else
  echo "FastAPI validation failed with HTTP status: $status"
  exit 1
fi
