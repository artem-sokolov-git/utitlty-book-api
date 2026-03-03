# Utility Book API

REST API сервис для учёта и контроля коммунальных расходов (электроэнергия и газ).

## Стек

- **Python** 3.12
- **Django** 5.2 + **Django Ninja** 1.5 (REST API)
- **PostgreSQL** 18 (хранилище данных)
- **uv** (управление зависимостями)
- **Docker** + **Docker Compose** (запуск среды)
- **Ruff** (линтер и форматтер)
- **pytest** (тесты)

## Структура проекта

```
src/
├── api/
│   └── readings/          # Ninja-роутеры и схемы для API
├── apps/
│   ├── common/            # Базовые модели (TimeBaseModel)
│   └── readings/          # Бизнес-логика: модели, querysets, admin
│       ├── admin/
│       ├── migrations/
│       ├── models/
│       └── querysets/
└── project/
    ├── settings/          # base.py + test.py
    ├── urls.py
    └── wsgi.py
docker/
├── apps.yaml              # Сервис api
└── storages.yaml          # Сервис pg
```

## Установка и запуск

### Требования

- Docker и Docker Compose
- [uv](https://docs.astral.sh/uv/) (для локальной разработки и тестов)

### 1. Настройка окружения

```bash
cp .env.example .env
```

Заполните `.env`:

```dotenv
## GENERAL
PROJECT_NAME="Utility Book API"
TZ="America/Toronto"
LANGUAGE_CODE="ru-ru"

## DJANGO SETTINGS
SECRET_KEY="your-secret-key"
DEBUG="true"
ALLOWED_HOSTS="localhost,127.0.0.1"

# Начальное показание газа по декларации
GAS_DEC_INITIAL_READING="0"

ADMIN_USER="admin"
ADMIN_PASSWORD="password"

## POSTGRES
POSTGRES_DB="utility_book"
POSTGRES_USER="postgres"
POSTGRES_PASSWORD="postgres"
POSTGRES_HOST="pg"
POSTGRES_PORT="5432"
```

### 2. Запуск через Docker

```bash
make run
```

Запускает контейнеры `pg` (PostgreSQL) и `api` (Django) в detached-режиме с пересборкой образа.

### 3. Применение миграций

```bash
make migrate
```

### 4. Создание суперпользователя

```bash
make superuser
```

После этого Django Admin доступен по адресу: [http://localhost:8000/admin/](http://localhost:8000/admin/)

### 5. Полная пересборка (dev)

Очищает тома, пересоздаёт контейнеры, применяет миграции, создаёт суперпользователя и загружает тестовые данные:

```bash
make rebuild
```

## API

Документация (Swagger UI): [http://localhost:8000/api/docs](http://localhost:8000/api/docs)

### Endpoints

#### Электроэнергия

```
GET /api/readings/electricity
```

| Параметр | Тип     | Описание                    |
|----------|---------|-----------------------------|
| `year`   | integer | Фильтр по году              |
| `month`  | integer | Фильтр по месяцу            |
| `last`   | boolean | Вернуть только последнюю запись |

**Пример ответа:**
```json
[
  {
    "id": 1,
    "reading_date": "2025-01-31",
    "reading_value": 15420,
    "unit_price": "4.32",
    "elect_reading_qty": 120,
    "total_elect_reading_sum": "518.40"
  }
]
```

#### Газ

```
GET /api/readings/gas
```

| Параметр | Тип     | Описание                    |
|----------|---------|-----------------------------|
| `year`   | integer | Фильтр по году              |
| `month`  | integer | Фильтр по месяцу            |
| `last`   | boolean | Вернуть только последнюю запись |

**Пример ответа:**
```json
[
  {
    "id": 1,
    "reading_date": "2025-01-31",
    "real_reading_value": 3250,
    "dec_reading_value": 3248,
    "dec_real_reading_diff": 2,
    "dec_reading_qty": 45,
    "dec_unit_price": "9.50",
    "total_dec_reading_sum": "427.50",
    "total_trans_sum": "58.20"
  }
]
```

## Make-команды

| Команда                    | Описание                                                    |
|----------------------------|-------------------------------------------------------------|
| `make run`                 | Запустить контейнеры (с пересборкой образа)                 |
| `make down`                | Остановить и удалить контейнеры                             |
| `make clear`               | Остановить контейнеры и удалить все тома                    |
| `make logs`                | Показать логи контейнеров                                   |
| `make migrate`             | Применить миграции                                          |
| `make migrations`          | Создать новые миграции                                      |
| `make superuser`           | Создать суперпользователя                                   |
| `make shell`               | Открыть Django shell                                        |
| `make check`               | Запустить ruff lint и format check                          |
| `make tests`               | Запустить тесты                                             |
| `make import-sql file=...` | Импортировать SQL-файл в базу данных                        |
| `make rebuild`             | Полная пересборка dev-окружения                             |

## Тесты

Тесты запускаются локально с использованием отдельной тестовой БД (поднимается через `docker/tests.yaml`):

```bash
make tests
```

Или напрямую через pytest (при уже запущенной тестовой БД):

```bash
uv run pytest
```

## Разработка

Установка зависимостей (включая dev-группу):

```bash
uv sync
```

Линтинг и форматирование:

```bash
make check                  # проверка
uv run ruff check --fix .   # автофикс линтинга
uv run ruff format .        # форматирование
```

Настройка pre-commit хуков:

```bash
uv run pre-commit install
```
