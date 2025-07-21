FROM alpine:latest

# Установка crond и необходимых инструментов
RUN apk add --no-cache bash curl postgresql-client busybox-suid
RUN apk add --no-cache tzdata
ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
# Копируем скрипты и задачи cron
COPY create_backup_all.sh /create_backup_all.sh
COPY backup_only_data.sh /backup_only_data.sh
COPY backup_only_schema.sh /backup_only_schema.sh
COPY backup.cron /etc/crontabs/root

RUN sed -i 's/\r$//' /create_backup_all.sh
RUN sed -i 's/\r$//' /backup_only_data.sh
RUN sed -i 's/\r$//' /backup_only_schema.sh

# Делаем скрипт исполняемым
RUN chmod +x /create_backup_all.sh
RUN chmod +x /backup_only_data.sh
RUN chmod +x /backup_only_schema.sh

# Команда запуска crond
CMD ["crond", "-f"]
