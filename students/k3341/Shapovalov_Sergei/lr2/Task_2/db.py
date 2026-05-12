import sys
from pathlib import Path

lr1_path = Path(__file__).parent.parent.parent / "lr1" / "Task_2-3"
sys.path.insert(0, str(lr1_path))

from sqlmodel import SQLModel, Session, create_engine
from models import Quote
import os
from dotenv import load_dotenv

env_path = lr1_path / ".env"
load_dotenv(env_path)
db_url = os.getenv('DB_URL')

if not db_url:
    raise ValueError("DATABASE URL not found in .env file")

engine = create_engine(db_url, echo=False)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    return Session(engine)


def save_quote(text: str, author: str, tags: str = ""):
    with get_session() as session:
        quote = Quote(text=text, author=author, tags=tags)
        session.add(quote)
        session.commit()
        session.refresh(quote)
        return quote


def clear_quotes():
    with get_session() as session:
        session.query(Quote).delete()
        session.commit()


def count_quotes():
    with get_session() as session:
        return session.query(Quote).count()
