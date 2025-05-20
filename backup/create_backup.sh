#!/bin/bash

# Параметры
BACKUP_DIR="/backups"
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
BACKUP_FILE="$BACKUP_DIR/db_backup_$TIMESTAMP.sql"

# Подключение
POSTGRES_USER="minatovar"
POSTGRES_PASSWORD="minatovarshop"
POSTGRES_DB="min_db"
POSTGRES_HOST="postgres"
POSTGRES_PORT="5432"

# Исключаемые таблицы (через пробел)
EXCLUDED_TABLES=""

# Формируем параметры исключения
EXCLUDE_ARGS=""
for TABLE in $EXCLUDED_TABLES; do
    EXCLUDE_ARGS+=" -T $TABLE"
done

# Проверяем папку для бэкапов
mkdir -p "$BACKUP_DIR"

# Создание бэкапа
export PGPASSWORD=$POSTGRES_PASSWORD
pg_dump -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -p "$POSTGRES_PORT" $EXCLUDE_ARGS > "$BACKUP_FILE"

if [ $? -eq 0 ]; then
  echo "Бэкап успешно сохранен: $BACKUP_FILE"
else
  echo "Ошибка создания бэкапа"
  [ -e "$BACKUP_FILE" ] && rm "$BACKUP_FILE"
fi

# Удаляем старые бэкапы (кроме 2 последних)
ls -tp "$BACKUP_DIR" | grep -v '/$' | tail -n +3 | xargs -I {} rm -- "$BACKUP_DIR/{}"