# Daemon ⚡

<p align="center">
  A modern habit tracking application built with <strong>FastAPI</strong>, <strong>SQLAlchemy</strong>, and <strong>Jinja2</strong>.
</p>

<p align="center">
  Track habits, log consistency, and manage progress through a clean dashboard interface.
</p>

---

## 🚀 Live Demo

🔗 [Visit Live Application](https://habit-tracker-api-lv5i.onrender.com)

📘 API Documentation:
- Swagger UI → `https://habit-tracker-api-lv5i.onrender.com/docs`
- ReDoc → `https://habit-tracker-api-lv5i.onrender.com/redoc`

---

## 🛠 Tech Stack

### Backend
- Python
- FastAPI
- SQLAlchemy
- Pydantic

### Frontend
- HTML
- CSS
- Jinja2 Templates

### Database
- SQLite

### Deployment
- Render

---

## ✨ Features

- Create new habits
- Update existing habits
- Delete habits
- Log daily habit completion
- View all habits
- View logs for individual habits
- Dashboard UI with server-side rendering
- RESTful API architecture
- SQLAlchemy ORM integration
- FastAPI automatic API docs
- Production deployment on Render

---

## 📂 Project Structure

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
├── requirements.txt
├── .env
└── README.md
```

---

# ⚙️ Installation

## 1. Clone Repository

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

### macOS/Linux

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

Create a `.env` file in the root directory:

```env
DATABASE_URL=sqlite:///orm_data.db
PORT=8000
```

---

## 5. Start Development Server

```bash
uvicorn main:app --reload
```

Server runs at:

```bash
http://127.0.0.1:8000
```

---

# 📡 API Endpoints

## Home Route

### `GET /`

Returns application status.

---

## Dashboard

### `GET /dashboard`

Renders the dashboard UI.

---

# 🧠 Habit Endpoints

## Create Habit

### `POST /habits`

### Request Body

```json
{
  "name": "Workout"
}
```

---

## Get All Habits

### `GET /habits`

---

## Get Single Habit

### `GET /habits/{name}`

Example:

```bash
/habits/Workout
```

---

## Update Habit

### `PUT /habits/{name}`

### Request Body

```json
{
  "name": "Workout",
  "name_to_update_to": "Gym"
}
```

---

## Delete Habit

### `DELETE /habits/{name}`

---

# 📅 Logs Endpoints

## Log Habit Completion

### `POST /logs/{habit_name_to_log}`

Example:

```bash
/logs/Workout
```

---

## Get Habit Logs

### `GET /logs/{habit}`

Example:

```bash
/logs/Workout
```

---

# 🗄 Database Models

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

# 📦 Example Requirements

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

# 🔮 Future Improvements

- JWT Authentication
- User Accounts
- Habit Streak Tracking
- Weekly Analytics
- PostgreSQL Migration
- Docker Support
- Mobile Responsive UI
- Habit Categories
- Notification System
- Background Task Scheduling

---

# 🚀 Deployment

This application is deployed on Render.

🔗 Production URL:
https://habit-tracker-api-lv5i.onrender.com

---

# 👨‍💻 Author

**Mikey**

Aspiring AI entrepreneur and developer.

---

# 📄 License

This project is licensed under the MIT License.

---