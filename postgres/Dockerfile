FROM alpine:latest

# Установка crond и необходимых инструментов
RUN apk add --no-cache bash curl postgresql-client busybox-suid
RUN apk add --no-cache tzdata
ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
# Копируем скрипты и задачи cron
COPY create_backup.sh /create_backup.sh
COPY backup.cron /etc/crontabs/root

# RUN sed -i 's/\r$//' /create_backup.sh

# Делаем скрипт исполняемым
RUN chmod +x /create_backup.sh

# Команда запуска crond
CMD ["crond", "-f"]
