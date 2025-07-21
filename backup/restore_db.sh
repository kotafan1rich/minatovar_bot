#!/bin/bash

# Parameters
CONTAINER_NAME="postgres"          # Container name from docker-compose.yml
BACKUP_DIR="./backup/backups"      # Folder with backups
POSTGRES_DB="min_db"               # Database name
POSTGRES_USER="minatovar"
POSTGRES_PASSWORD="minatovarshop"  # User password

# Check if backup folder exists
if [ ! -d "$BACKUP_DIR" ]; then
  echo "Backup folder not found: $BACKUP_DIR"
  exit 1
fi

# Show available backups
echo "Available backups:"
ls -1 $BACKUP_DIR/*.sql || { echo "No backups found in $BACKUP_DIR"; exit 1; }

# Ask user to choose a file
echo -n "Enter the filename to restore (with .sql extension): "
read BACKUP_FILE

# Check if the specified file exists
if [ ! -f "$BACKUP_DIR/$BACKUP_FILE" ]; then
  echo "File not found: $BACKUP_DIR/$BACKUP_FILE"
  exit 1
fi

# Start restoring the database
echo "Starting database restore from file $BACKUP_DIR/$BACKUP_FILE..."

docker exec -e PGPASSWORD=$POSTGRES_PASSWORD -i $CONTAINER_NAME psql -U $POSTGRES_USER -d $POSTGRES_DB < "$BACKUP_DIR/$BACKUP_FILE"

# Check if restore was successful
if [ $? -eq 0 ]; then
  echo "Restore completed successfully."
else
  echo "Database restore error."
fi