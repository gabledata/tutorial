#!/bin/bash

echo "Starting Hive"
pkill -f /opt/hive/bin/hive || true
/entrypoint.sh &
echo "Hive initialization was successful."

echo "Waiting for Hive server to start..."
SUCCESS=0
ATTEMPTS=0
MAX_ATTEMPTS=30 

while [ $SUCCESS -eq 0 -a $ATTEMPTS -lt $MAX_ATTEMPTS ]; do
  echo "Attempting to connect to Hive server (Attempt $((ATTEMPTS+1))/$MAX_ATTEMPTS)..."
  if echo "SHOW DATABASES;" | beeline -u jdbc:hive2://localhost:10000 > /dev/null 2>&1; then
    SUCCESS=1
    echo "Hive server is up and running."
  else
    ATTEMPTS=$((ATTEMPTS+1))
    sleep 2 
  fi
done

if [ $SUCCESS -eq 0 ]; then
  echo "Failed to connect to Hive server after $MAX_ATTEMPTS attempts."
  exit 1
fi

echo "Seeding Hive database..."

beeline -u jdbc:hive2://localhost:10000 -n root -p '' -f /opt/hive-scripts/seed_hive.txt

echo "Database seeded."

# Keep the container running until stopped
tail -f /dev/null