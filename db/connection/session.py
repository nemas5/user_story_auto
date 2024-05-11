from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from config import get_db_settings
from db.models import Base

settings = get_db_settings()
DATABASE_URL = settings.db_url

engine = create_engine(DATABASE_URL)
session = sessionmaker(engine, class_=Session)


def init_db() -> None:

    with engine.begin() as conn:
        conn.run_sync(Base.metadata.drop_all)
        conn.run_sync(Base.metadata.create_all)


def get_session() -> Generator[Session, None]:

    with session() as sess:
        return sess
