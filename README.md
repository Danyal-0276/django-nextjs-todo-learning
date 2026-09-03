# Django + Next.js Todo Learning Project

[![Django](https://img.shields.io/badge/Django-6.1-0C4B33?logo=django)](https://www.djangoproject.com/) [![Next.js](https://img.shields.io/badge/Next.js-16-black?logo=next.js)](https://nextjs.org/) [![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?logo=typescript)](https://www.typescriptlang.org/) [![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-4-06B6D4?logo=tailwindcss)](https://tailwindcss.com/) [![Learning Project](https://img.shields.io/badge/status-learning_project-ff6b4a)](#project-status)

A beginner-friendly full-stack Todo application for learning Django REST APIs, Next.js integration, PostgreSQL, JWT authentication, and user authorization.

The repository deliberately separates the existing server-rendered Django application from a new Next.js frontend. The frontend currently uses local mock state; REST endpoints, PostgreSQL, CORS, and JWT are planned exercises rather than finished features.

## Learning objectives

- Understand how a browser frontend sends requests to a backend API.
- Model and validate data with Django and Django REST Framework (DRF).
- Authenticate users with access and refresh JWTs.
- Enforce authorization so each user sees only their own todos.
- Move development data from SQLite to PostgreSQL.
- Handle loading, validation, and API failures in a typed Next.js UI.

## Project status

### Implemented

- Existing Django templates, user signup/login views, sessions, and per-user todo model.
- Next.js App Router frontend with TypeScript, Tailwind CSS, and ESLint.
- Responsive login, signup, dashboard, loading, empty, feedback, and not-found views.
- Frontend add, edit, complete/uncomplete, and delete interactions using React state.
- Typed API client, auth/todo service contracts, and token-storage learning boilerplate.

### Mocked

- Frontend authentication accepts locally validated demo input and navigates to the dashboard.
- Todos reset to sample data on refresh.
- No frontend request currently reaches Django.

### Planned

- DRF serializers, viewsets, routers, CRUD endpoints, PostgreSQL, Simple JWT, permissions, CORS, tests, and deployment.

> The legacy Django UI has known learning-project issues: its login view shadows Django's `login` helper, signup reads the wrong email field, edit/delete lookups are not scoped to the current user, deletion uses GET, and templates reference a missing `status` field. These files are intentionally preserved for the learner to improve.

## Technology stack

- **Backend:** Python, Django 6.1.1, SQLite (current)
- **Frontend:** Next.js 16 App Router, React 19, TypeScript, Tailwind CSS 4
- **Planned:** Django REST Framework, PostgreSQL, Simple JWT, django-cors-headers

## Project structure

```text
.
├── todo/                         # Existing Django project (unchanged)
│   ├── manage.py
│   └── todo/
│       ├── migrations/
│       ├── static/
│       ├── templates/
│       ├── models.py
│       ├── settings.py
│       ├── urls.py
│       └── views.py
├── frontend/                     # New Next.js frontend
│   ├── public/
│   └── src/
│       ├── app/                  # Routes: login, signup, todos, 404
│       ├── components/           # Auth, layout, todo, and UI components
│       ├── hooks/                # Mock todo state
│       ├── lib/                  # API client and token helper
│       ├── services/             # Future auth/todo API calls
│       └── types/                # Shared TypeScript contracts
├── .env.example
├── .gitignore
├── LEARNING_ROADMAP.md
└── README.md
```

## Backend setup (Windows PowerShell)

From the repository root:

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install Django==6.1.1
Copy-Item todo\todo\settings.example.py todo\todo\settings.py # only after a fresh clone
cd todo
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000/`. If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process Bypass` for that terminal session and retry activation.

The original local `settings.py` is ignored because it contains a hard-coded secret and was not modified. A clone uses `settings.example.py`; set `DJANGO_SECRET_KEY` before any non-local deployment.

## Frontend setup

In a second terminal:

```powershell
cd frontend
Copy-Item .env.example .env.local
npm install
npm run dev
```

Open `http://localhost:3000/`. The API URL placeholder is configured with `NEXT_PUBLIC_API_BASE_URL` in `frontend/.env.local`; changing it has no visible effect until mock handlers are replaced with service calls.

Useful checks:

```powershell
cd todo
..\venv\Scripts\python.exe manage.py check

cd ..\frontend
npm run lint
npm run build
```

## Proposed API (not implemented)

| Method | Endpoint | Purpose | Authentication |
|---|---|---|---|
| POST | `/api/auth/register/` | Create a user | Public |
| POST | `/api/auth/token/` | Obtain access and refresh tokens | Public |
| POST | `/api/auth/token/refresh/` | Refresh an access token | Refresh token |
| GET | `/api/todos/` | List the current user's todos | Access token |
| POST | `/api/todos/` | Create a todo owned by the current user | Access token |
| GET | `/api/todos/{id}/` | Read one owned todo | Access token |
| PATCH | `/api/todos/{id}/` | Edit or toggle one owned todo | Access token |
| DELETE | `/api/todos/{id}/` | Delete one owned todo | Access token |

## Planned authentication flow

1. Registration sends validated user details to Django.
2. Login sends credentials to the token endpoint.
3. Django returns short-lived access and longer-lived refresh tokens.
4. The client sends `Authorization: Bearer <access-token>` on protected requests.
5. On expiry, the client exchanges the refresh token for a new access token and retries once.
6. Django permissions and queryset filtering enforce ownership; hiding UI is not authorization.
7. Logout clears client tokens and, if implemented later, blacklists the refresh token.

Token storage in this project is only a commented learning starting point. Review XSS, CSRF, secure cookies, token rotation, and logout behavior before choosing a production design.

## Roadmap

The detailed, command-by-command curriculum is in [LEARNING_ROADMAP.md](LEARNING_ROADMAP.md). Broad phases are: stabilize the existing backend, introduce PostgreSQL and DRF, build/test CRUD, add JWT and ownership permissions, configure CORS, connect the frontend services, then test and deploy.

## Screenshots

Add real screenshots after running the frontend:

- `docs/screenshots/login.png` — login page
- `docs/screenshots/signup.png` — registration page
- `docs/screenshots/dashboard.png` — todo dashboard

## Future improvements

- Persist filters and due dates, add pagination, and improve optimistic updates.
- Add unit, API, component, and end-to-end tests.
- Adopt secure production settings, secrets management, logging, and CI.
- Deploy PostgreSQL, Django, and Next.js with HTTPS.

## Contributing

This repository is primarily a guided learning project. Open an issue before large changes, create a focused branch, keep secrets and generated files out of commits, run both backend and frontend checks, and describe what you learned in the pull request.

## License

No license has been selected yet. Until one is added, normal copyright rules apply and reuse is not automatically granted.
