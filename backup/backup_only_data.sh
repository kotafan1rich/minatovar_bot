#!/bin/bash

BACKUP_DIR="/backups"
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
DATA_BACKUP_FILE="$BACKUP_DIR/data_backup_$TIMESTAMP.sql"

EXCLUDED_TABLES="alembic_version"

# Формируем параметры исключения
EXCLUDE_ARGS=""
for TABLE in $EXCLUDED_TABLES; do
    EXCLUDE_ARGS+=" -T $TABLE"
done

mkdir -p "$BACKUP_DIR"

export PGPASSWORD=$POSTGRES_PASSWORD
pg_dump -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_NAME" -p "$POSTGRES_PORT" \
  --data-only $EXCLUDE_ARGS > "$DATA_BACKUP_FILE"

if [ $? -eq 0 ]; then
  echo "Бэкап данных успешно сохранен: $DATA_BACKUP_FILE"
else
  echo "Ошибка создания бэкапа данных"
  [ -e "$DATA_BACKUP_FILE" ] && rm "$DATA_BACKUP_FILE"
  exit 1
fi

find "$BACKUP_DIR" -name "data_backup_*.sql*" -type f | \
    sort -r | \
    tail -n +$(($MAX_BACKUPS + 1)) | \
    xargs -r rm -f --

echo "Готово! Оставлены последние 2 бэкапа данных."
