# Smart Interview Evaluation Assistant — Backend

Django REST API for interview evaluation: token authentication, PostgreSQL persistence, and AI-assisted candidate report generation.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create a [Neon](https://neon.tech) project, copy the connection details into `.env`, then run migrations:

```powershell
python manage.py migrate
python seed_data.py
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8000
```

## Environment

Create a `.env` file in this folder (not committed to Git). Use values from **Neon → Dashboard → Connection details**:

```env
DJANGO_SECRET_KEY=your-random-secret
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost,*

GEMINI_API_KEY=your-api-key
GEMINI_API_URL=https://api.openai.com/v1/chat/completions
GEMINI_MODEL=gemini-1.5-pro

DB_ENGINE=django.db.backends.postgresql
DB_NAME=neondb
DB_USER=your-neon-user
DB_PASSWORD=your-neon-password
DB_HOST=ep-xxxx.region.aws.neon.tech
DB_PORT=5432
DB_SSLMODE=require
```

`DB_SSLMODE=require` is required for Neon. For local PostgreSQL only, use `DB_HOST=localhost` and omit `DB_SSLMODE` or set `prefer`.

## API

Base URL: `http://127.0.0.1:8000/api`

- `POST /auth/signup/` — register
- `POST /auth/login/` — login (returns token)
- `GET/POST /evaluations/` — list / create evaluations
- `GET/PATCH/DELETE /evaluations/{id}/` — read / update verdict / delete
- `GET /evaluations/current-user/` — current user profile

## Related repo

Frontend: [Smart-Interview-Evaluation-Assistant-Frontend](https://github.com/CodewithHassan1/Smart-Interview-Evaluation-Assistant-Frontend)
