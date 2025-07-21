FROM python:3.10-bullseye

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Обновляем пакеты и устанавливаем зависимости
RUN apt-get update && \
apt-get upgrade -y && \
apt-get install -y --no-install-recommends \
gcc \
tzdata \
libpq-dev \
build-essential \
libxml2-dev \
libxslt-dev && \
rm -rf /var/lib/apt/lists/* && \
pip install poetry

# Устанавливаем часовой пояс
ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Копируем файлы зависимостей
COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --only main

COPY . .

ENV PYTHONPATH=/app

# Даем права на выполнение скриптов
RUN chmod a+x docker/*.sh

