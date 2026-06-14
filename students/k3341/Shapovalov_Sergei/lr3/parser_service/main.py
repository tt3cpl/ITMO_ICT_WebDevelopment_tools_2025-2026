import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Parser Service")


class ParseRequest(BaseModel): # модель для тела входящего запроса
    url: str


class QuoteItem(BaseModel): # модели для ответа
    text: str
    author: str
    tags: str


class ParseResponse(BaseModel):
    message: str
    url: str
    quotes_found: int
    quotes: List[QuoteItem]


@app.get("/")  # эндпоинт для проверки что сервис живой
def health():
    return {"status": "ok", "service": "parser"}


@app.post("/parse", response_model=ParseResponse) # oсновной эндпоинт. пост потому что передаем данные в теле. 
def parse(data: ParseRequest):
    try:
        response = requests.get(data.url, timeout=10) # загружаем страницу с таймаутом в 10 секунд 
        response.raise_for_status()
    except requests.RequestException as e: #если что-то пошло не так, возвращаем 500 с описанием ошибки
        raise HTTPException(status_code=500, detail=f"Ошибка URL: {str(e)}")

    soup = BeautifulSoup(response.content, "html.parser") # парсим HTML 
    quote_divs = soup.find_all("div", class_="quote") # находим все <div class="quote">

    quotes = []
    for q in quote_divs:
        text_elem = q.find("span", class_="text") # для каждой div ищем блоки text, author, tag 
        author_elem = q.find("small", class_="author")
        tag_elems = q.find_all("a", class_="tag")

        text = text_elem.get_text(strip=True) if text_elem else "" # вытаскивает текст без HTML-тегов и text_elem else если если элемент не найден на будущее 
        author = author_elem.get_text(strip=True) if author_elem else "Unknown"
        tags = ", ".join(t.get_text(strip=True) for t in tag_elems)

        quotes.append(QuoteItem(text=text, author=author, tags=tags)) # ну и добавляем

    return ParseResponse( # возвращаем результат FastAPI сам сериализует объект в JSON
        message="Parsing completed",
        url=data.url,
        quotes_found=len(quotes),
        quotes=quotes)
