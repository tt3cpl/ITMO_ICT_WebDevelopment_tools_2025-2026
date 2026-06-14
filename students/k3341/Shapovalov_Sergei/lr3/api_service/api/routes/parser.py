import os
import requests as http_requests
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from sqlmodel import Session
from connection import get_session
from models import Quote
from tasks import parse_url_task
from celery_app import celery_app

PARSER_SERVICE_URL = os.getenv("PARSER_SERVICE_URL", "http://parser:8001")

router = APIRouter(prefix="/parser", tags=["Parser"]) # создаем роутер FastAPI все маршруты будут начинаться с /parser


class ParseRequest(BaseModel): # модель входных данных
    url: str


class QuoteOut(BaseModel): # модель ответа для цитаты
    id: Optional[int]
    text: str
    author: str
    tags: Optional[str]

    class Config: # разрешает создавать Pydantic-модель
        from_attributes = True


# синхронный вызов парсера
@router.post("/parse", summary="Синхронный парсинг URL")
def parse_sync(data: ParseRequest, session: Session = Depends(get_session)):  # тело запроса + сессия БД
    try:
        response = http_requests.post( # отправляем URL сервису парсера
            f"{PARSER_SERVICE_URL}/parse",
            json={"url": data.url},
            timeout=30)
        response.raise_for_status()
    except http_requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Ошибка парса: {str(e)}")

    result = response.json() #преобразуем JSON-ответ
    quotes = result.get("quotes", []) # получаем список цитат
    saved = []
    for q in quotes: # перебираем найденные цитаты
        quote = Quote(text=q["text"], author=q["author"], tags=q["tags"]) # для каждой div ищем блоки text, author, tag 
        session.add(quote) # добавляем объект в сессию
        session.flush() # немедленно отправляем INSERT в БД
        saved.append(quote) # сохраняем объект в список
    session.commit()

    return { # возвращаем ответ
        "message": "Parsing completed",
        "url": data.url,
        "quotes_found": result.get("quotes_found", 0),
        "quotes_saved": len(saved),
        "quotes": [{"text": q.text, "author": q.author, "tags": q.tags} for q in saved]}


# асинхронный вызов через Celery 
@router.post("/parse/async", summary="Асинхронный парсинг через очередь Celery")
def parse_async(data: ParseRequest):
    task = parse_url_task.delay(data.url) # создаем задачу и отправляем ее в Redis
    return { 
        "message": "Task queued",
        "task_id": task.id, # уникальный идентификатор задачи
        "url": data.url,  # URL который будет обработан
        "status_url": f"/parser/parse/status/{task.id}"} # адрес для проверки статуса

# проверка статуса
@router.get("/parse/status/{task_id}", summary="Статус асинхронной задачи")
def get_task_status(task_id: str):
    result = celery_app.AsyncResult(task_id) # находим задачу по ID
    response = {"task_id": task_id, "status": result.status} # базовый ответ

    if result.ready(): # если задача завершена
        if result.successful(): # если завершилась успешно
            response["result"] = result.get() # получаем return из Celery-задачи
        else:
            response["error"] = str(result.result) # если была ошибка

    return response


# Просмотр сохраненных цитат

@router.get("/quotes", response_model=List[QuoteOut], summary="Все сохранённые цитаты")
def get_quotes(session: Session = Depends(get_session)):
    return session.query(Quote).all() # SELECT * FROM quotes
