import os
from celery import Celery

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0") # читаем URL Redis. /0 в конце это номер базы данных Redis всего их 16 от 0 до 15

celery_app = Celery( # создаем объект Celery
    "lab3",
    broker=REDIS_URL, # broker куда Celery отправляет задачи
    backend=REDIS_URL, # куда сохраняет результаты выполненных задач
    include=["tasks"]) # список модулей где искать задачи

celery_app.conf.update( # настройки
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Europe/Moscow",
    enable_utc=True,
    result_expires=3600) # хранятся в Redis 1 час. удаляются автоматически
