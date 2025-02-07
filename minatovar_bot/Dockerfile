# Строим образ с зависимостями
FROM python:3.9-slim AS builder

WORKDIR /app

# Отключаем запись байт-кода, чтобы не засорять контейнер
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
rm -rf /var/lib/apt/lists/*


# Обновляем pip и создаем колеса для зависимостей
COPY requirements.txt . 
RUN python3 -m pip install --upgrade pip && \
pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Финальный этап
FROM python:3.9-bullseye

WORKDIR /app

# Копируем зависимости из builder
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt . 

ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Устанавливаем зависимости из wheels
RUN python3 -m pip install --no-cache-dir /wheels/*

# Копируем остальные файлы
COPY . .

# Даем права на выполнение скриптов
RUN chmod a+x docker/*.sh