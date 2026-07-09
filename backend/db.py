from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os
from dotenv import load_dotenv

load_dotenv()
DB_URL = os.getenv("DATABASE_URL")
engine = create_engine(DB_URL)
SessinLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessinLocal()
    try:
        yield db
    finally:
        db.close()
