from app.database import Base
from app.dependencies import get_db
from app.main import app
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

engine = create_engine(
    "sqlite:///:memory", connect_args={"check_same_thread": False}, poolclass=StaticPool
)
LocalTestSession = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)

client = TestClient(app)


def override_get_db():
    db = LocalTestSession()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "the table has been created and running"}


def test_create_habit():
    response = client.post("/habits", json={"name": "jerk_off"})
    assert response.status_code == 200
    assert response.json() == {"message": "a new habit jerk_off is created"}


def test_get_one_habit():
    client.post("/habits", json={"name": "jerk_off"})
    response = client.get("/habits/jerk_off")
    assert response.status_code == 200
