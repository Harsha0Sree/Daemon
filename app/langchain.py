import os

from app.database import SessionLocal
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from app.models import Habit, VoiceWorkout
from sqlalchemy import desc, select

load_dotenv()

model = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    model="nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
    api_key=os.environ.get("OPEN_ROUTER_API_KEY"),
)

system_prompt = """Your are an intelligent useful assistant that helps in my daily tasks and answer my questions"""


@tool
def query_latest_workout() -> str:
    """Use this tool to retrieve the user's latest logged workout including exercise name and reps performed."""
    with SessionLocal() as session:
        stmt = select(VoiceWorkout).order_by(desc(VoiceWorkout.id)).limit(1)
        row = session.execute(stmt).scalar_one_or_none()
        if row is not None:
            return f"you have performed {row.reps_performed} of {row.name_of_exercise}"
        else:
            return "no workout data found"


@tool
def query_habits() -> str:
    """use this tool to get all of the habits of the user only"""
    with SessionLocal() as session:
        result = session.execute(select(Habit)).scalars().all()
        habits_list = []
        if result:
            for habit in result:
                habits_list.append(habit.habit_name)
            return f"this is the list of habit of the user:{habits_list}"
        return "there are no habits"


agent = create_agent(
    model=model,
    tools=[query_latest_workout, query_habits],
    system_prompt=system_prompt,
)


result = agent.invoke(
    {
        "messages": [
            {"role": "user", "content": "summarise my habits and workouts"},
        ]
    }
)

print(result["messages"])
