# DAEMON

Behavioral operating system that enforces habit completion before internet access is restored.

DAEMON combines AI agents, voice transcription, analytics, scheduling, and OS-level website blocking into a self-regulation backend platform.

---

# Problem Statement

Most productivity systems rely on reminders and self-discipline.

DAEMON approaches the problem differently:

* distracting websites remain blocked
* habits must be completed first
* workouts and actions can be logged through voice
* analytics provide behavioral feedback loops
* automation maintains enforcement in the background

The project is designed as a backend-heavy behavioral infrastructure system rather than a simple CRUD tracker.

---

# Features

* Voice-based workout logging using AssemblyAI transcription
* AI oracle agent using LangChain tools + OpenRouter LLMs
* OS-level website blocking through hosts file manipulation
* Habit-gated internet unlock system
* Workout analytics using Pandas
* Background automation using APScheduler
* Dockerized PostgreSQL deployment
* FastAPI REST API architecture
* SQLAlchemy ORM integration
* Jinja-powered dashboard rendering

---

# Architecture

```mermaid
graph TD

A[Frontend Dashboard] --> B[FastAPI Backend]

B --> C[(PostgreSQL)]
B --> D[AssemblyAI API]
B --> E[LangChain Agent]
B --> F[Gatekeeper]
B --> G[Scheduler]
B --> H[Pandas Analytics]

F --> I["/etc/hosts"]
```

---

# Tech Stack

| Layer            | Technology  |
| ---------------- | ----------- |
| Backend          | FastAPI     |
| ORM              | SQLAlchemy  |
| Database         | PostgreSQL  |
| AI Framework     | LangChain   |
| Transcription    | AssemblyAI  |
| Scheduling       | APScheduler |
| Analytics        | Pandas      |
| Templating       | Jinja2      |
| Containerization | Docker      |

---

# Project Structure

```text
daemon/
├── app/
│   ├── main.py              # FastAPI entrypoint
│   ├── models.py            # ORM + Pydantic schemas
│   ├── database.py          # SQLAlchemy engine/session
│   ├── assemblyai.py        # Voice transcription pipeline
│   ├── analytics.py         # Workout analytics using Pandas
│   ├── gatekeeper.py        # OS-level website blocking
│   ├── scheduler.py         # APScheduler jobs
│   ├── dependencies.py      # Dependency injection
│   └── templates/           # Jinja dashboard views
│
├── screenshots/
├── tests/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

---

# Installation

## Clone Repository

```bash
git clone <repo_url>
cd daemon
```

---

## Create Environment Variables

Create a `.env` file:

```env
DATABASE_URL=postgresql://postgres:password@postgres:5432/app_db
ASSEMBLY_API_KEY=your_key
OPEN_ROUTER_API_KEY=your_key
```

---

## Run With Docker

```bash
docker-compose up --build
```

---

## Access Services

```text
FastAPI API: http://localhost:8000
Swagger Docs: http://localhost:8000/docs
PostgreSQL: localhost:5432
```

---

# API Examples

## Create Habit

```http
POST /habits
```

### Request

```json
{
  "name": "meditate"
}
```

### Response

```json
{
  "message": "a new habit meditate is created"
}
```

---

## Voice Workout Logging

```http
POST /voice_log
```

### Form Data

```text
audio=<audio_file>
```

### Pipeline

```text
Audio Upload
→ AssemblyAI Transcription
→ Regex Parsing
→ Database Insert
→ Analytics Update
```

---

# Screenshots

Add screenshots inside the `/screenshots` directory.

Recommended captures:

* dashboard UI
* Swagger API docs
* Docker containers running
* blocked website behavior
* analytics output

---

# Current Limitations

## Regex-Based Parsing

The workout extraction pipeline currently relies on regex parsing and may fail on ambiguous natural language.

### Example Edge Cases

```text
"I did 50 pushups and 20 pullups"
"completed fifty pushups"
```

---

## Hosts File Safety

Website blocking currently writes directly to `/etc/hosts`.

Future production hardening should include:

* atomic writes
* managed sections
* automatic backups

---

## Import-Time Agent Execution

LangChain agent invocation should be isolated from module imports to avoid startup-side effects and deployment instability.

---

# Future Improvements

* Replace regex parsing with structured LLM extraction
* Add Redis task queue
* Add authentication + multi-user support
* Add websocket dashboard updates
* Add ML-based behavioral predictions
* Add cloud deployment pipeline
* Add observability and metrics

---

# Lessons Learned

* Lifecycle management in FastAPI
* ORM relationship handling in SQLAlchemy
* Dockerized backend orchestration
* API polling workflows using AssemblyAI
* Scheduler design for long-running services
* Risks of side effects during application startup
* System-level architecture design across multiple subsystems

---

# Repository Goals

DAEMON is designed to demonstrate:

* backend systems engineering
* infrastructure-aware application design
* AI-assisted automation
* behavioral systems architecture
* production-oriented API structure

---

# License

MIT License
