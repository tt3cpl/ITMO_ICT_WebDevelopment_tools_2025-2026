from fastapi import FastAPI
from connection import init_db
from api.routes import parser

# Импортируем роуты из lr1 (уже были реализованы там)
# добавляем только роуты парсера
app = FastAPI(title="Lab3 API Service") 


@app.get("/") # самый простой маршрут для проверки работы сервиса
def hello():
    return {"message": "Hello! Lab3 API is running."}


@app.on_event("startup") # выполняется один раз при старте FastAPI
def on_startup():
    init_db()


app.include_router(parser.router) # все маршруты из parser.router становятся частью API
