habit_tracker

## Описание

Проект для отслеживания привычек с использованием Django, Celery, Redis и PostgreSQL.

## Технологии
1. Backend: Django + DRF.
2. База данных: PostgreSQL
3. Кеширование и брокер сообщений: Redis
4. Асинхронные задачи: Celery
5. Веб-сервер: Nginx.
6. Контейнеризация: Docker + Docker Compose
7. CI/CD: GitHub Actions

## Локальный запуск проекта

### Предварительные требования
1. Docker и Docker Compose установлены на вашей системе.
2. Git для клонирования репозитория

```
sudo apt update
sudo apt install git
git --version

```

### Шаги для запуска
1. Клонируйте репозиторий
```
sudo mkdir -p /var/www/habit_tracker
cd /var/www/habit_tracker
git clone --mirror https://github.com/albinakazartseva2215/habit_tracker.git

```
2. Создайте .env и вставьте секретные данные.
```
sudo nano /var/www/habit_tracker/.env

```
3. Запустите проект с помощью Docker Compose:
```
docker-compose up -d --build

```
4. Проект будет доступен по адресу: http://server_IP:8000
5. Остановка проекта:
```
docker-compose down

```

## Деплой на сервер
### Настройка сервера
Подготовьте сервер с установленными Docker и Docker Compose

Настройте SSH-доступ к серверу

Убедитесь, что открыты необходимые порты (80, 443, 22)

### Настройка CI/CD
В репозитории GitHub перейдите в Settings → Secrets → Actions

Добавьте следующие секреты:

DEPLOY_DIR: Путь к директории проекта на сервере (/var/www/habit_tracker)

DEPLOY_HOST: IP-адрес или домен сервера

DEPLOY_USER: Пользователь для SSH-соединения

DEPLOY_SSH_KEY: Приватный SSH-ключ для доступа к серверу

PROD_SECRET_KEY: Секретный ключ Django для production

PROD_DB_PASSWORD: Пароль для production базы данных

PROD_ALLOWED_HOSTS: Домен/IP сервера для ALLOWED_HOSTS

### Процесс деплоя
При пуше в ветку Develop автоматически запускается процесс CI/CD:

Тестирование: Запуск unit-тестов и проверка кода

Сборка: Проверка возможности сборки Docker-образов

Деплой: Развертывание на сервере с помощью Docker Compose как ожидалось.


## Адрес сервера
Проект развернут по адресу:  http://your-server-ip