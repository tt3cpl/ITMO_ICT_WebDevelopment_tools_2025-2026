# Lab 3 — FastAPI + Docker + Celery + Redis

## Структура проекта

```
lab3/
├── docker-compose.yml          # Оркестрация всех сервисов
├── api_service/                # Основное FastAPI приложение
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py                 # Точка входа
│   ├── connection.py           # Подключение к PostgreSQL
│   ├── models.py               # SQLModel модели (из lr1)
│   ├── celery_app.py           # Конфигурация Celery
│   ├── tasks.py                # Celery-задача парсинга
│   ├── .env
│   ├── api/routes/
│   │   └── parser.py           # Эндпоинты парсера
│   └── services/
│       ├── security.py
│       └── deps.py
└── parser_service/             # Отдельный сервис парсера
    ├── Dockerfile
    ├── requirements.txt
    └── main.py                 # FastAPI с эндпоинтом /parse
```

## Запуск

```bash
cd lab3
docker-compose up --build
```

## API эндпоинты

После запуска документация доступна на:
- **API**: http://localhost:8000/docs
- **Parser**: http://localhost:8001/docs

### Подзадача 2 — Синхронный парсинг

```
POST http://localhost:8000/parser/parse
Content-Type: application/json

{"url": "https://quotes.toscrape.com/"}
```

Ответ — сразу список найденных и сохранённых цитат.

### Подзадача 3 — Асинхронный парсинг через очередь

**Запустить задачу:**
```
POST http://localhost:8000/parser/parse/async
Content-Type: application/json

{"url": "https://quotes.toscrape.com/"}
```

Ответ: `{"task_id": "abc-123", "status_url": "/parser/parse/status/abc-123"}`

**Проверить статус:**
```
GET http://localhost:8000/parser/parse/status/{task_id}
```

**Посмотреть сохранённые цитаты:**
```
GET http://localhost:8000/parser/quotes
```

## Сервисы в docker-compose

| Сервис         | Порт  | Описание                        |
|----------------|-------|---------------------------------|
| `db`           | 5432  | PostgreSQL база данных          |
| `redis`        | 6379  | Redis брокер для Celery         |
| `parser`       | 8001  | Сервис парсера quotes.toscrape  |
| `api`          | 8000  | Основное FastAPI приложение     |
| `celery_worker`| —     | Celery воркер (фоновые задачи)  |
