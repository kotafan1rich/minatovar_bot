#!/bin/bash

# Параметры
BACKUP_DIR="/backups"
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
BACKUP_FILE="$BACKUP_DIR/db_backup_$TIMESTAMP.sql"

# Подключение
POSTGRES_USER="postgres"
POSTGRES_PASSWORD="2007Fj2007"
POSTGRES_DB="min_db"
POSTGRES_HOST="postgres"

# Проверяем, существует ли папка для бэкапов
if [ ! -d "$BACKUP_DIR" ]; then
  mkdir -p "$BACKUP_DIR"
fi

# Создание бэкапа
export PGPASSWORD=$POSTGRES_PASSWORD
pg_dump -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" > "$BACKUP_FILE"

if [ $? -eq 0 ]; then
  echo "Бэкап успешно сохранен: $BACKUP_FILE"
else
  echo "Ошибка создания бэкапа"
  [ -e "$BACKUP_FILE" ] && rm "$BACKUP_FILE"
fi

# Удаляем все, кроме двух последних бэкапов
ls -tp "$BACKUP_DIR" | grep -v '/$' | tail -n +3 | xargs -I {} rm -- "$BACKUP_DIR/{}"
