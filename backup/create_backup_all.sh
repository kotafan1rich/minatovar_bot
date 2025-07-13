#!/bin/bash

BACKUP_DIR="/backups"
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
DATA_BACKUP_FILE="$BACKUP_DIR/data_backup_$TIMESTAMP.sql"
SCHEMA_BACKUP_FILE="$BACKUP_DIR/schema_backup_$TIMESTAMP.sql"
export PGPASSWORD=$POSTGRES_PASSWORD

# Параметры
EXCLUDED_TABLES="alembic_version"

# Формируем параметры исключения
EXCLUDE_ARGS=""
for TABLE in $EXCLUDED_TABLES; do
    EXCLUDE_ARGS+=" -T $TABLE"
done

mkdir -p "$BACKUP_DIR"

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

EXCLUDED_TABLES=""

# Формируем параметры исключения
EXCLUDE_ARGS=""
for TABLE in $EXCLUDED_TABLES; do
    EXCLUDE_ARGS+=" -T $TABLE"
done

# Проверяем папку для бэкапов
mkdir -p "$BACKUP_DIR"

# 1. Бэкап только структуры (схемы без данных)
pg_dump -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_NAME" -p "$POSTGRES_PORT" \
  --schema-only $EXCLUDE_ARGS > "$SCHEMA_BACKUP_FILE"

if [ $? -eq 0 ]; then
  echo "Бэкап структуры успешно сохранен: $SCHEMA_BACKUP_FILE"
else
  echo "Ошибка создания бэкапа структуры"
  [ -e "$SCHEMA_BACKUP_FILE" ] && rm "$SCHEMA_BACKUP_FILE"
  exit 1
fi

ls -tp "$BACKUP_DIR/schema_backup_"* 2>/dev/null | tail -n +3 | xargs -I {} rm -- {}

echo "Готово! Оставлены последние 2 бэкапа схем"
