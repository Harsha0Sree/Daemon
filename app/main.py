import os
from contextlib import asynccontextmanager
from datetime import date

from app.assemblyai import process_voice_data
from app.database import Base, engine
from app.dependencies import get_db
from app.gatekeeper import (
    block_websites,
    check_unlock_status,
    sync_blocked_sites,
    unblock_websites,
)
from app.models import (
    Habit,
    HabitCreate,
    HabitToUpdate,
    Logs,
    VoiceWorkout,
    WebsiteList,
    WebsitesToBlock,
)
from app.scheduler import register_jobs, scheduler
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, File, Form, Request, UploadFile
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

load_dotenv()

PORT = os.environ.get("PORT", 8000)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        Base.metadata.create_all(engine)
    except OperationalError:
        print("postgres container not runnning specified port")
        raise RuntimeError("Database startup failed")
    register_jobs()
    scheduler.start()

    yield

    scheduler.shutdown()

    print("app shutting down")


app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
def home():
    return {"message": "the table has been created and running"}


@app.get("/dashboard")
def get_dashboard(request: Request, db: Session = Depends(get_db)):
    row = select(Habit)
    habits = db.execute(row).scalars().all()
    return templates.TemplateResponse(
        request=request, name="dashboard.html", context={"habits": habits}
    )


@app.post("/habits")
def create_habit(habit: HabitCreate, db: Session = Depends(get_db)):
    new_row = Habit(habit_name=habit.name)
    db.add(new_row)
    db.commit()

    return {
        "message": f"a new habit {habit.name} is created",
    }


@app.get("/habits")
def get_all_habits(db: Session = Depends(get_db)):

    row = select(Habit)
    habits = db.execute(row).scalars().all()

    return {"data": habits}


@app.get("/habits/{name}")
def get_one_habit(name: str, db: Session = Depends(get_db)):
    row = select(Habit).where(Habit.habit_name == name)
    habit = db.execute(row).scalar_one_or_none()

    if habit is None:
        return "habit not found"
    return {"id": habit.id, "name": habit.habit_name}


@app.delete("/habits/{name}")
def delete_habit(name: str, db: Session = Depends(get_db)):
    row = select(Habit).where(Habit.habit_name == name)
    habit_to_delete = db.execute(row).scalar_one_or_none()
    if habit_to_delete is not None:
        db.delete(habit_to_delete)
        db.commit()
        return {"message": f"the habit {name} is deleted"}
    return {"message": f"habit {name} not found"}


@app.post("/logs/{habit_name_to_log}")
def log_habit(habit_name_to_log: str, db: Session = Depends(get_db)):
    row = select(Habit).where(Habit.habit_name == habit_name_to_log)
    habit = db.execute(row).scalar_one_or_none()

    if habit is not None:
        today_date = date.today()
        logs = Logs(habit_id=habit.id, logs=today_date)
        db.add(logs)
        db.commit()
        return {
            "message": f"the habit {habit_name_to_log} has been logged on {today_date}"
        }
    return {"message": "no logs found"}


@app.get("/logs/{habit}")
def get_logs(habit: str, db: Session = Depends(get_db)):
    row = select(Habit).where(Habit.habit_name == habit)
    habit = db.execute(row).scalar_one_or_none()
    log_row = select(Logs).where(Logs.habit_id == habit.id)
    logs = db.execute(log_row).scalars().all()
    return {"data": logs}


@app.post("/habits/create")
def create_habit_new(habit_name: str = Form(...), db: Session = Depends(get_db)):
    new_habit = Habit(habit_name=habit_name)
    db.add(new_habit)
    db.commit()
    return RedirectResponse(url="/dashboard", status_code=303)


@app.put("/habits/{name}")
def update_habit(name_to_update_to: HabitToUpdate, db: Session = Depends(get_db)):
    row = select(Habit).where(Habit.habit_name == name_to_update_to.name)
    habit = db.execute(row).scalar_one_or_none()
    if habit is not None:
        habit.habit_name = name_to_update_to.name_to_update_to
        db.commit()

    return {
        "message": f"the habit {name_to_update_to.name} has been changed to {name_to_update_to.name_to_update_to} "
    }


@app.post("/voice_log")
async def voice_transcript(
    audio: UploadFile = File(...), db: Session = Depends(get_db)
):
    reps, exercise = process_voice_data(audio)

    if reps is not None and exercise is not None:
        result = VoiceWorkout(
            name_of_exercise=exercise, reps_performed=reps, timestamp=date.today()
        )
        db.add(result)
        db.commit()

        return {"message": f"the {exercise} has been logged with {reps} reps"}
    return {"message": "not able to parse the transcript"}


@app.post("/websites_to_block")
def add_websites_to_block(
    websites_to_block: WebsiteList, db: Session = Depends(get_db)
):
    for website in websites_to_block.websites:
        new_obj = WebsitesToBlock(url=website)
        db.add(new_obj)
        db.commit()
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
        return {"message": "unlocked"}

    return {"message": "finish habits"}
