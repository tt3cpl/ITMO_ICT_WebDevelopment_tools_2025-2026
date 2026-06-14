import os
from sqlmodel import SQLModel, Session, create_engine
from dotenv import load_dotenv

load_dotenv()

db_url = os.getenv("DB_URL", "postgresql+psycopg2://postgres:postgres@db:5432/lab3_db")
engine = create_engine(db_url, echo=True) # создаем движок SQL 


def init_db():
    SQLModel.metadata.create_all(engine) # создаем все таблицы в базе данных по описанным моделям


def get_session():
    with Session(engine) as session:
        yield session
