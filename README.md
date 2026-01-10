# FastAPI Application

Бэкенд приложение на FastAPI с чистой архитектурой.

## Структура проекта

```
omd/
├── api/                    # API роутеры и эндпоинты
│   └── v1/
│       ├── api.py         # Главный роутер API v1
│       └── endpoints/     # Эндпоинты
├── core/                   # Конфигурация и настройки
│   └── config.py          # Настройки приложения
├── database/               # Настройки базы данных
│   └── base.py            # Базовые настройки БД
├── models/                 # SQLAlchemy модели
│   ├── base.py            # Базовые модели
│   └── example.py         # Пример модели
├── schemas/                # Pydantic схемы
│   └── example.py         # Пример схем
├── services/               # Бизнес-логика
│   └── example_service.py # Пример сервиса
├── main.py                 # Точка входа приложения
├── requirements.txt        # Зависимости
└── .env.example           # Пример файла с переменными окружения
```

## Установка

1. Создайте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # для Linux/Mac
# или
venv\Scripts\activate  # для Windows
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Создайте файл `.env` на основе `.env.example`:
```bash
cp .env.example .env
```

4. Запустите приложение:
```bash
uvicorn main:app --reload
```

Приложение будет доступно по адресу: http://localhost:8000

## Документация API

После запуска приложения документация доступна по адресам:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Основные компоненты

- **models/** - SQLAlchemy модели для работы с базой данных
- **schemas/** - Pydantic схемы для валидации данных
- **services/** - Бизнес-логика приложения
- **api/** - Роутеры и эндпоинты API
- **database/** - Настройки подключения к базе данных
- **core/** - Конфигурация приложения
