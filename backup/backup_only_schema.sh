#!/bin/bash

BACKUP_DIR="/backups"
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
SCHEMA_BACKUP_FILE="$BACKUP_DIR/schema_backup_$TIMESTAMP.sql"

EXCLUDED_TABLES=""

# Generate exclude parameters
EXCLUDE_ARGS=""
for TABLE in $EXCLUDED_TABLES; do
    EXCLUDE_ARGS+=" -T $TABLE"
done

# Check backup directory
mkdir -p "$BACKUP_DIR"

# 1. Backup only schema (structure without data)
export PGPASSWORD=$POSTGRES_PASSWORD
pg_dump -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_NAME" -p "$POSTGRES_PORT" \
  --schema-only $EXCLUDE_ARGS > "$SCHEMA_BACKUP_FILE"

if [ $? -eq 0 ]; then
  echo "Schema backup successfully saved: $SCHEMA_BACKUP_FILE"
else
  echo "Error creating schema backup"
  [ -e "$SCHEMA_BACKUP_FILE" ] && rm "$SCHEMA_BACKUP_FILE"
  exit 1
fi

ls -tp "$BACKUP_DIR/schema_backup_"* 2>/dev/null | tail -n +3 | xargs -I {} rm -- {}

echo "Done! Only the last 2 schema backups are kept."