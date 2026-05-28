# DAEMON

> Behavioral operating system that enforces habit completion before internet access is restored.

DAEMON is a backend-heavy behavioral infrastructure system that combines AI agents, voice transcription, analytics, scheduling, and OS-level website blocking into a self-regulation platform.

## Live Deployment

* 🚀 Live API: https://habit-tracker-api-lv5i.onrender.com
* 📘 Swagger Docs: https://habit-tracker-api-lv5i.onrender.com/docs

---

# Why I Built This

Most habit trackers fail because they rely on willpower.

I wanted a system that enforced behavioral constraints beneath the browser layer itself.

Instead of tracking habits passively, DAEMON actively modifies system behavior by blocking distracting websites until required habits are completed.

The project evolved into a full-stack behavioral enforcement engine integrating:

* AI-powered voice logging
* relational state management
* automation workflows
* analytics pipelines
* OS-level controls
* containerized deployment

---

# Core Features

## Behavioral Enforcement

* OS-level website blocking using hosts-file manipulation
* Habit-gated internet unlock system
* Automated block reset scheduling

---

## AI + Voice Logging

* Voice-based workout logging using AssemblyAI
* LangChain-powered AI oracle agent
* OpenRouter LLM integration
* Natural-language workout parsing pipeline

---

## Analytics + Automation

* Workout analytics using Pandas
* Automated streak tracking
* APScheduler background jobs
* Dashboard visualization support

---

## Backend Infrastructure

* FastAPI REST API architecture
* SQLAlchemy ORM integration
* PostgreSQL database support
* Dependency injection patterns
* Dockerized deployment

---

# Architecture

```mermaid
graph TD

A[Frontend Dashboard] --> B[FastAPI Backend]

B --> C[(PostgreSQL)]
B --> D[AssemblyAI API]
B --> E[LangChain Agent]
B --> F[Gatekeeper Engine]
B --> G[APScheduler]
B --> H[Pandas Analytics]

F --> I["/etc/hosts"]
```

---

# System Flow

```mermaid
graph LR

A[User Opens Distracting Website] --> B[Website Blocked]

B --> C[Complete Habit]
C --> D[Habit Stored in Database]
D --> E[Unlock Endpoint Triggered]
E --> F[Hosts File Updated]
F --> G[Website Access Restored]
```

---

# Tech Stack

| Layer                  | Technology    |
| ---------------------- | ------------- |
| Backend Framework      | FastAPI       |
| ORM                    | SQLAlchemy    |
| Database               | PostgreSQL    |
| AI Framework           | LangChain     |
| LLM Provider           | OpenRouter    |
| Voice Transcription    | AssemblyAI    |
| Scheduling             | APScheduler   |
| Analytics              | Pandas        |
| Templates              | Jinja2        |
| Containerization       | Docker        |
| Environment Management | python-dotenv |
| Deployment             | Render        |

---

# Repository Structure

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

# Demo Flow

## 1. Dashboard

Visualize:

* streaks
* analytics
* blocked sites
* behavioral progress

---

## 2. Voice Workout Logging

User says:

```text
"I did 50 pushups"
```

Pipeline:

```text
Audio Upload
→ AssemblyAI Transcription
→ Regex Parsing
→ Database Insert
→ Analytics Update
```

---

## 3. Gatekeeper Enforcement

Attempting to open a blocked website fails until the required habit is completed.

This creates actual behavioral enforcement instead of passive tracking.

---

## 4. Habit Completion

```text
Habit Completed
→ Unlock Endpoint Triggered
→ Hosts File Updated
→ Website Access Restored
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

| Service      | URL                        |
| ------------ | -------------------------- |
| FastAPI API  | http://localhost:8000      |
| Swagger Docs | http://localhost:8000/docs |
| PostgreSQL   | localhost:5432             |

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

---

## Unlock Internet Access

```http
POST /unlock
```

### Behavior

```text
Checks habit completion state
→ Removes blocked entries
→ Restores website access
```

---

# Docker Commands

## Build + Run Containers

```bash
docker-compose up --build
```

---

## View Running Containers

```bash
docker ps
```

---

## View Logs

```bash
docker logs <container_id>
```

---

# Deployment

## Render Deployment

DAEMON is deployed on Render.

### Production URL

https://habit-tracker-api-lv5i.onrender.com

### Interactive API Docs

https://habit-tracker-api-lv5i.onrender.com/docs

---

# Screenshots

Create a `/screenshots` directory and include:

* dashboard UI
* Swagger documentation
* Docker containers running
* analytics visualizations
* blocked website behavior
* voice logging flow

Recommended additions:

* GIF demo
* terminal walkthrough
* architecture image

---

# Current Limitations

## Regex-Based Parsing

Workout extraction currently relies on regex parsing and can fail on ambiguous language.

Example edge cases:

```text
"I did 50 pushups and 20 pullups"

"completed fifty pushups"
```

Future versions should use structured LLM extraction pipelines.

---

## Hosts File Safety

Current website blocking directly modifies `/etc/hosts`.

Production hardening should include:

* atomic writes
* rollback backups
* managed sections
* corruption recovery

---

## Import-Time Side Effects

LangChain agent execution should not occur during module import.

Startup-time execution creates:

* nondeterministic boot behavior
* deployment instability
* API dependency risks

---

# Future Improvements

* Replace regex parsing with structured LLM extraction
* Add Redis task queue
* Add authentication + multi-user support
* Add websocket dashboard updates
* Add ML-based behavioral predictions
* Add cloud deployment pipeline
* Add observability and metrics
* Add usage telemetry
* Add mobile companion app
* Add browser extension integration

---

# Lessons Learned

This project involved system-level engineering across:

* API architecture
* ORM modeling
* relational databases
* scheduling systems
* AI tooling
* Docker deployment
* analytics pipelines
* OS-level system manipulation
* background automation
* infrastructure debugging

Key technical takeaways:

* lifecycle management in FastAPI
* ORM relationship handling in SQLAlchemy
* API polling architecture from AssemblyAI
* scheduler orchestration patterns
* containerized backend deployment
* risks of side effects during startup
* designing coherent multi-system architectures

---

# What This Project Demonstrates

DAEMON demonstrates:

* backend systems engineering
* infrastructure-aware architecture
* AI-assisted automation
* system-level behavioral enforcement
* multi-service orchestration
* production-oriented API design
* independent problem selection
* end-to-end execution capability

---

# Repository Goals

This repository is intended to showcase:

* systems thinking
* architectural reasoning
* backend engineering depth
* behavioral systems design
* deployment capability
* technical communication

---

# License

MIT License
