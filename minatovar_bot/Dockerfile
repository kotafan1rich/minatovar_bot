FROM python:3.9.21-slim-bookworm 
RUN mkdir /app

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Устанавливаем зависимости
RUN pip install -r requirements.txt

# Копируем исходный код бота в контейнер
COPY . .
# Команда для запуска бота
RUN chmod a+x docker/*.sh
