# Pipeline Management Platform

Платформа запуска и мониторинга бизнес-пайплайнов на FastAPI с PostgreSQL.

## Структура проекта

```
backend/
├── alembic/                # Миграции базы данных
├── api/                    # API роутеры и эндпоинты
│   └── v1/
│       ├── api.py         # Главный роутер API v1
│       └── endpoints/     # Эндпоинты
├── core/                   # Конфигурация и настройки
│   └── config.py          # Настройки приложения
├── database/               # Настройки базы данных
│   ├── base.py            # Базовые настройки БД
│   └── annotations.py     # Кастомные типы (GUID)
├── models/                 # SQLAlchemy модели
│   ├── __init__.py        # Экспорт моделей
│   ├── base.py            # Базовая модель
│   ├── user.py            # Модель пользователя
│   └── pipeline.py        # Модель пайплайна
├── schemas/                # Pydantic схемы
│   ├── user.py
│   └── pipeline.py
├── services/               # Бизнес-логика
├── main.py                 # Точка входа приложения
├── requirements.txt        # Зависимости
└── docker-compose.yml      # Docker Compose для PostgreSQL
```

## Установка и запуск

### 1. Установите зависимости

```bash
cd backend
pip install -r requirements.txt
```

### 2. Запустите PostgreSQL

```bash
docker-compose up -d
```

Это запустит PostgreSQL с параметрами:
- Host: `localhost`
- Port: `5432`
- User: `omd_user`
- Password: `omd_password`
- Database: `omd_db`

### 3. Создайте файл `.env`

Скопируйте `.env.example` и настройте под свои нужды:

```bash
cp .env.example .env
```

### 4. Создайте миграции

```bash
alembic revision --autogenerate -m "Initial migration"
```

### 5. Примените миграции

```bash
alembic upgrade head
```

### 6. Запустите приложение

```bash
uvicorn main:app --reload
```

Приложение будет доступно по адресу: http://localhost:8000

## Документация API

После запуска приложения документация доступна по адресам:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Модели

### User
- `id` (UUID) - уникальный идентификатор
- `email` - email пользователя
- `password_hash` - хеш пароля
- `is_active` - активен ли пользователь
- `role` - роль (admin/user)
- `created_at` - дата создания
- `updated_at` - дата обновления

### Pipeline
- `id` (UUID) - уникальный идентификатор
- `name` - название пайплайна
- `code` - уникальный код
- `description` - описание
- `executor_type` - тип исполнителя (airflow)
- `external_id` - внешний ID (dag_id)
- `is_active` - активен ли пайплайн
- `created_at` - дата создания
- `updated_at` - дата обновления

## Полезные команды

### Alembic

```bash
# Создать новую миграцию
alembic revision --autogenerate -m "Description"

# Применить миграции
alembic upgrade head

# Откатить миграцию
alembic downgrade -1

# Показать историю миграций
alembic history

# Показать текущую версию
alembic current
```

### Docker

```bash
# Запустить PostgreSQL
docker-compose up -d

# Остановить PostgreSQL
docker-compose down

# Просмотр логов
docker-compose logs -f postgres

# Подключиться к PostgreSQL
docker exec -it omd_postgres psql -U omd_user -d omd_db
```

## Разработка

- Python 3.10+
- PostgreSQL 16
- FastAPI
- SQLAlchemy 2.0
- Alembic
