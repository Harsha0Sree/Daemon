# Daemon - Habit Tracker API

A modern habit tracking web application built with **FastAPI**, **SQLAlchemy**, and **Jinja2 Templates**.  
Daemon allows users to create habits, track daily completions, manage logs, and visualize habits through a clean dashboard UI.

## Live Demo

🌐 Deployed Application:  
[Live Application](https://habit-tracker-api-lv5i.onrender.com)

---

# Features

- Create habits
- Update existing habits
- Delete habits
- Log daily habit completion
- View all habits
- View logs for individual habits
- Dashboard UI with Jinja2 templates
- SQLite database integration
- SQLAlchemy ORM
- RESTful API endpoints
- Render deployment support

---

# Tech Stack

## Backend
- Python
- FastAPI
- SQLAlchemy
- Pydantic

## Frontend
- HTML
- CSS
- Jinja2 Templates

## Database
- SQLite

## Deployment
- Render

---

# Project Structure

```bash
project/
│
├── core/
│   ├── templates/
│   │   └── dashboard.html
│   │
│   ├── static/
│   │   └── dashboard.css
│   │
│   ├── database.py
│   └── models.py
│
├── main.py
├── .env
├── requirements.txt
└── README.md
```

---

# Installation

## 1. Clone the Repository

```bash
git clone https://github.com/your-username/daemon-habit-tracker.git
cd daemon-habit-tracker
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Mac/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create a `.env` file:

```env
DATABASE_URL=sqlite:///orm_data.db
PORT=8000
```

---

## 5. Run the Server

```bash
uvicorn main:app --reload
```

Server will run on:

```bash
http://127.0.0.1:8000
```

---

# API Endpoints

## Home

### GET `/`

Returns application status.

---

## Dashboard

### GET `/dashboard`

Renders the habit tracking dashboard UI.

---

# Habit Endpoints

## Create Habit

### POST `/habits`

### Request Body

```json
{
  "name": "Workout"
}
```

---

## Get All Habits

### GET `/habits`

---

## Get One Habit

### GET `/habits/{name}`

Example:

```bash
/habits/Workout
```

---

## Update Habit

### PUT `/habits/{name}`

### Request Body

```json
{
  "name": "Workout",
  "name_to_update_to": "Gym"
}
```

---

## Delete Habit

### DELETE `/habits/{name}`

---

# Logs Endpoints

## Log Habit Completion

### POST `/logs/{habit_name_to_log}`

Example:

```bash
/logs/Workout
```

---

## Get Habit Logs

### GET `/logs/{habit}`

Example:

```bash
/logs/Workout
```

---

# Database Models

## Habit Model

```python
class Habit(Base):
    __tablename__ = "habits"

    habit_name: Mapped[str] = mapped_column(unique=True)
    id: Mapped[int] = mapped_column(primary_key=True)
```

---

## Logs Model

```python
class Logs(Base):
    __tablename__ = "logs"

    habit_id: Mapped[int] = mapped_column(ForeignKey("habits.id"))
    logs: Mapped[str]
    id: Mapped[int] = mapped_column(primary_key=True)
```

---

# UI Preview

The dashboard includes:

- Habit statistics
- Habit cards
- Completion buttons
- Habit creation form
- Modern dark-themed interface

---

# Future Improvements

- User authentication
- JWT authorization
- Habit streak tracking
- Weekly/monthly analytics
- PostgreSQL support
- Docker deployment
- Responsive mobile UI
- Habit categories
- Notifications and reminders

---

# Requirements

Example `requirements.txt`

```txt
fastapi
uvicorn
sqlalchemy
jinja2
python-dotenv
pydantic
python-multipart
```

---

# Deployment

This project is deployed on Render.

Production URL:[Visit Live App](https://habit-tracker-api-lv5i.onrender.com)

---

# Author

Mikey

---

# License

This project is open source and available under the MIT License.