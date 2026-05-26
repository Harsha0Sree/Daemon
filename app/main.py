import os
from contextlib import asynccontextmanager
from datetime import date

from app.assemblyai import process_voice_data
from app.database import Base, SessionLocal, engine
from app.gatekeeper import block_websites, sync_blocked_sites, unblock_websites,check_unlock_status
from app.models import Habit, Logs, VoiceWorkout, WebsitesToBlock
from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, Request, UploadFile
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import OperationalError

load_dotenv()

PORT = os.environ.get("PORT", 8000)


class HabitCreate(BaseModel):
    name: str


class HabitToUpdate(BaseModel):
    name: str
    name_to_update_to: str


class WebsiteList(BaseModel):
    websites: list


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        Base.metadata.create_all(engine)
    except OperationalError:
        print("postgres container not runnning specified port")
        raise RuntimeError("Database startup failed")
    yield

    print("app shutting down")


app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory="core/templates")
app.mount("/static", StaticFiles(directory="core/static"), name="static")


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


@app.post("/voice_log")
async def voice_transcript(audio: UploadFile = File(...)):
    reps, exercise = process_voice_data(audio)

    if reps is not None and exercise is not None:
        with SessionLocal() as session:
            result = VoiceWorkout(
                name_of_exercise=exercise, reps_performed=reps, timestamp=date.today()
            )
            session.add(result)
            session.commit()

        return {"message": f"the {exercise} has been logged with {reps} reps"}
    return {"message": "not able to parse the transcript"}


@app.post("/websites_to_block")
def add_websites_to_block(websites_to_block: WebsiteList):
    with SessionLocal() as session:
        for website in websites_to_block.websites:
            new_obj = WebsitesToBlock(url=website)
            session.add(new_obj)
            session.commit()
    block_websites(websites_to_block.websites)
    return {"message": "websites have been added to block list"}


@app.post("/unblock_websites")
def unblock_websites_endpoint(websites_to_unblock: WebsiteList):
    unblock_websites(websites_to_unblock.websites)
    return {"message": "the websites have been removed from block"}


@app.post("/sync_blocked_websites")
def sync_block_list():
    sync_blocked_sites()
    return {"message": "synced"}


@app.post("/unlock")
def unlock_previlage():
    if check_unlock_status():
        unblock_websites()
        return {"message":"unlocked"}
        
    return {"message":"finish habits"}