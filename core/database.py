import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


class Base(DeclarativeBase):
    pass


load_dotenv()
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///orm_data.db")

engine = create_engine(DATABASE_URL, echo=True)


SessionLocal = sessionmaker(bind=engine)
