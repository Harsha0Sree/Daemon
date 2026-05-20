from database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class Habit(Base):
    __tablename__ = "habits"
    habit_name: Mapped[str] = mapped_column(unique=True)
    id: Mapped[int] = mapped_column(primary_key=True)


class Logs(Base):
    __tablename__ = "logs"
    habit_id: Mapped[int] = mapped_column(ForeignKey("habits.id"))
    logs: Mapped[str]
    id: Mapped[int] = mapped_column(primary_key=True)
