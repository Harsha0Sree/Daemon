from datetime import date

from app.database import Base
from sqlalchemy import Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Habit(Base):
    __tablename__ = "habits"
    habit_name: Mapped[str] = mapped_column(unique=True)
    id: Mapped[int] = mapped_column(primary_key=True)
    is_required: Mapped[bool] = mapped_column(Boolean, default=False)
    logs = relationship("Logs", back_populates="habit",order_by="Logs.logs")


class Logs(Base):
    __tablename__ = "habit_logs"
    habit_id: Mapped[int] = mapped_column(ForeignKey("habits.id"))
    logs: Mapped[date]
    id: Mapped[int] = mapped_column(primary_key=True)
    habit = relationship("Habit", back_populates="logs")


class VoiceWorkout(Base):
    __tablename__ = "voice_workout"
    name_of_exercise: Mapped[str] = mapped_column(unique=True)
    reps_performed: Mapped[int]
    timestamp: Mapped[date]
    id: Mapped[int] = mapped_column(primary_key=True)


class WebsitesToBlock(Base):
    __tablename__ = "blocklist"
    url: Mapped[str] = mapped_column(unique=True)
    id: Mapped[int] = mapped_column(primary_key=True)
