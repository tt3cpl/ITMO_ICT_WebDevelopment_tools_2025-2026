import os
import requests as http_requests
from celery_app import celery_app
from connection import get_session # функция получения сессии БД
from models import Quote

PARSER_URL = os.getenv("PARSER_SERVICE_URL", "http://parser:8001") # адрес сервиса парсера


@celery_app.task(bind=True, name="tasks.parse_url") # превращает обычную функцию в Celery задачу
def parse_url_task(self, url: str):
    try:
        response = http_requests.post( # воркер делает HTTP-запрос к сервису парсера с переданным URL
            f"{PARSER_URL}/parse",
            json={"url": url},
            timeout=30)
        response.raise_for_status()
        data = response.json()

        saved = 0
        session_gen = get_session()
        session = next(session_gen) # первый next() дает нам сессию
        try:
            for q in data.get("quotes", []):
                quote = Quote(text=q["text"], author=q["author"], tags=q["tags"])
                session.add(quote) 
            session.commit() # один commit() это эффективнее чем коммитить каждую по отдельности
            saved = len(data.get("quotes", [])) # считаем количество сохраненных цитат
        finally:
            try:
                next(session_gen) # завершаем сессию 
            except StopIteration:
                pass

        return { # результат успешного выполнения задачи
            "status": "success",
            "url": url,
            "quotes_found": data.get("quotes_found", 0),
            "quotes_saved": saved}

    except Exception as exc: # если возникла любая ошибка то Celery повторит задачу через 5 секунд максимум 3 раза
        raise self.retry(exc=exc, countdown=5, max_retries=3)
