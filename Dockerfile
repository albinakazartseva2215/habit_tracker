FROM python:3.13-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Устанавливаем зависимости системы
RUN apt-get update \
    && apt-get install -y gcc libpq-dev\
    postgresql-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем poetry
RUN pip install poetry

# Копируем зависимости
COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости
RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-ansi --no-root

# Копируем исходный код приложения в контейнер
COPY . .

# Копируем .env файл
# COPY .env /app/.env

# Создаем директорию для медиафайлов
RUN mkdir -p /app/media

# Создаем и даем права на директорию для статических файлов
RUN mkdir -p /app/staticfiles && chmod -R 755 /app/staticfiles

# Пробрасываем порт, который будет использовать Django
EXPOSE 8000

# Команда для запуска приложения
CMD ["sh", "-c", "python manage.py collectstatic --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:8000"]