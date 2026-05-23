# Smart Interview Evaluation Assistant — Backend

Django REST API for interview evaluation: token authentication, PostgreSQL persistence, and AI-assisted candidate report generation.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create the PostgreSQL database, then run migrations:

```powershell
psql -U postgres -c "CREATE DATABASE interview_evaluation;"
python manage.py migrate
python seed_data.py
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8000
```

## Environment

Copy `.env.example` to `.env` and set:

- `DJANGO_SECRET_KEY` — random secret for production
- `GEMINI_API_KEY` — API key for AI report generation
- `DB_*` — PostgreSQL connection settings

## API

Base URL: `http://127.0.0.1:8000/api`

- `POST /auth/signup/` — register
- `POST /auth/login/` — login (returns token)
- `GET/POST /evaluations/` — list / create evaluations
- `GET/PATCH/DELETE /evaluations/{id}/` — read / update verdict / delete
- `GET /evaluations/current-user/` — current user profile

## Related repo

Frontend: [Smart-Interview-Evaluation-Assistant-Frontend](https://github.com/CodewithHassan1/Smart-Interview-Evaluation-Assistant-Frontend)
