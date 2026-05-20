import os
from datetime import date

from core.database import Base, SessionLocal, engine
from dotenv import load_dotenv
from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from core.models import Habit, Logs
from pydantic import BaseModel
from sqlalchemy import select

load_dotenv()

PORT = os.environ.get("PORT", 8000)

Base.metadata.create_all(engine)


class HabitCreate(BaseModel):
    name: str


class HabitToUpdate(BaseModel):
    name: str
    name_to_update_to: str


app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def home():
    return {"message": "the table has been created and running"}


@app.get("/dashboard")
def get_dashboard(request: Request):
    with SessionLocal() as session:
        row = select(Habit)
        habits = session.execute(row).scalars().all()
        return templates.TemplateResponse(
            request=request, name="dashboard.html", context={"habits": habits}
        )


@app.post("/habits")
def create_habit(habit: HabitCreate):
    with SessionLocal() as session:
        new_row = Habit(habit_name=habit.name)
        session.add(new_row)
        session.commit()

    return {
        "message": f"a new habit {habit} is created",
    }


@app.get("/habits")
def get_all_habits():
    with SessionLocal() as session:
        row = select(Habit)
        habits = session.execute(row).scalars().all()

    return {"data": habits}


@app.get("/habits/{name}")
def get_one_habit(name: str):
    with SessionLocal() as session:
        row = select(Habit).where(Habit.habit_name == name)
        habit = session.execute(row).scalar_one_or_none()

        if habit is None:
            return "habit not found"
        return {"id": habit.id, "name": habit.habit_name}


@app.delete("/habits/{name}")
def delete_habit(name: str):
    with SessionLocal() as session:
        row = select(Habit).where(Habit.habit_name == name)
        habit_to_delete = session.execute(row).scalar_one_or_none()
        if habit_to_delete is not None:
            session.delete(habit_to_delete)
            session.commit()
            return {"message": f"the habit {name} is deleted"}
        return {"message": f"habit {name} not found"}


@app.post("/logs/{habit_name_to_log}")
def log_habit(habit_name_to_log: str):
    with SessionLocal() as session:
        row = select(Habit).where(Habit.habit_name == habit_name_to_log)
        habit = session.execute(row).scalar_one_or_none()

        if habit is not None:
            today_date = str(date.today())
            logs = Logs(habit_id=habit.id, logs=today_date)
            session.add(logs)
            session.commit()
            return {
                "message": f"the habit {habit_name_to_log} has been logged on {today_date}"
            }
        return {"message": "no logs found"}


@app.get("/logs/{habit}")
def get_logs(habit: str):
    with SessionLocal() as session:
        row = select(Habit).where(Habit.habit_name == habit)
        habit = session.execute(row).scalar_one_or_none()
        log_row = select(Logs).where(Logs.habit_id == habit.id)
        logs = session.execute(log_row).scalars().all()
    return {"data": logs}


@app.post("/habits/create")
def create_habit_new(habit_name: str = Form(...)):
    with SessionLocal() as session:
        new_habit = Habit(habit_name=habit_name)
        session.add(new_habit)
        session.commit()
    return RedirectResponse(url="/dashboard", status_code=303)


@app.put("/habits/{name}")
def update_habit(name_to_update_to: HabitToUpdate):
    with SessionLocal() as session:
        row = select(Habit).where(Habit.habit_name == name_to_update_to.name)
        habit = session.execute(row).scalar_one_or_none()
        if habit is not None:
            habit.habit_name = name_to_update_to.name_to_update_to
            session.commit()

        return {
            "message": f"the habit {name_to_update_to.name} has been changed to {name_to_update_to.name_to_update_to} "
        }
