from fastapi import Depends
from sqlmodel import SQLModel, Session, create_engine
import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)
db_url = os.getenv('DB_URL')

if not db_url:
    raise ValueError("DATABASE URL not found in .env file")

engine = create_engine(db_url, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
