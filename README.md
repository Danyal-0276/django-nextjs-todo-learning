# Django + Next.js Todo Learning Project

[![Django](https://img.shields.io/badge/Django-6.1-0C4B33?logo=django)](https://www.djangoproject.com/) [![Next.js](https://img.shields.io/badge/Next.js-16-black?logo=next.js)](https://nextjs.org/) [![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?logo=typescript)](https://www.typescriptlang.org/) [![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-4-06B6D4?logo=tailwindcss)](https://tailwindcss.com/) [![Learning Project](https://img.shields.io/badge/status-learning_project-ff6b4a)](#project-status)

A beginner-friendly full-stack Todo application for learning Django REST APIs, Next.js integration, PostgreSQL, JWT authentication, and user authorization.

The repository deliberately separates the server-rendered Django application from a Next.js frontend. The Django backend uses PostgreSQL and exposes registration, JWT authentication, and user-scoped Todo REST endpoints. The Next.js signup and login forms now call the real Django API, while the Todo dashboard still uses local mock state until the next learning phase.

## Learning objectives

- Understand how a browser frontend sends requests to a backend API.
- Model and validate data with Django and Django REST Framework (DRF).
- Authenticate users with access and refresh JWTs.
- Enforce authorization so each user sees only their own todos.
- Move development data from SQLite to PostgreSQL.
- Handle loading, validation, and API failures in a typed Next.js UI.

## Project status

### Implemented

- Django templates, validated user signup/login, session authentication, and secure per-user Todo CRUD.
- PostgreSQL persistence through Django's ORM and environment-based database configuration.
- Django REST Framework serializer, viewset, router, protected Todo CRUD endpoints, and per-user queryset filtering.
- Simple JWT access-token login, refresh, verification, and Bearer-token authentication.
- Backend model, authentication, template-view, authorization, REST API, JWT, registration, and CORS tests (62 total).
- Public REST registration with password confirmation, Django password validation, and unique-email validation.
- CORS restricted to the local Next.js origins and `/api/` routes.
- Next.js App Router frontend with TypeScript, Tailwind CSS, and ESLint.
- Responsive login, signup, dashboard, loading, empty, feedback, and not-found views.
- Frontend add, edit, complete/uncomplete, and delete interactions using React state.
- Typed API client, real frontend registration/JWT login, token storage, logout, and a basic client-side dashboard guard.
- Todo service contracts prepared for the next integration phase.

### Mocked

- Todos reset to sample data on refresh.
- The dashboard greeting and Todo interactions still use frontend-only data.

### Planned

- Connecting the Todo dashboard to the Django API.
- Automatic access-token refresh and optional refresh-token blacklisting.
- Frontend component/integration tests, CI, and deployment.

## Technology stack

- **Backend:** Python, Django 6.1.1, Django REST Framework 3.18.1, Simple JWT 5.5.1, PostgreSQL
- **Frontend:** Next.js 16 App Router, React 19, TypeScript, Tailwind CSS 4
- **Integration status:** authentication connected; Todo API connection, automatic token refresh, automated frontend tests, and deployment remain planned

## Project structure

```text
.
├── todo/                         # Django backend
│   ├── manage.py
│   └── todo/
│       ├── migrations/
│       ├── static/
│       ├── templates/
│       ├── tests/                # Model, HTML view, API, and JWT tests
│       ├── api_urls.py           # REST Todo router
│       ├── api_views.py          # User-scoped REST Todo viewset
│       ├── models.py
│       ├── serializers.py        # Todo JSON validation/representation
│       ├── settings.py
│       ├── urls.py
│       └── views.py
├── frontend/                     # New Next.js frontend
│   ├── public/
│   └── src/
│       ├── app/                  # Routes: login, signup, todos, 404
│       ├── components/           # Auth, layout, todo, and UI components
│       ├── hooks/                # Mock todo state awaiting API integration
│       ├── lib/                  # API client and token storage helper
│       ├── services/             # Auth and Todo API request functions
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
python -m pip install -r requirements.txt
Copy-Item todo\todo\settings.example.py todo\todo\settings.py # only after a fresh clone
Copy-Item .env.example .env
# Replace placeholder values in .env with your local PostgreSQL credentials.
cd todo
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000/`. If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process Bypass` for that terminal session and retry activation.

The tracked settings read Django and PostgreSQL values from the untracked root `.env`. Never commit `.env`, real database passwords, JWTs, or production secret keys.

## Frontend setup

In a second terminal:

```powershell
cd frontend
Copy-Item .env.example .env.local
npm install
npm run dev
```

Open `http://localhost:3000/`. `NEXT_PUBLIC_API_BASE_URL` in `frontend/.env.local` tells the signup and login forms where to reach Django. Restart the development server after changing this value.

Useful checks:

```powershell
cd todo
..\venv\Scripts\python.exe manage.py check

cd ..\frontend
npm run lint
npm run build
```

## API status

| Method | Endpoint | Purpose | Authentication |
|---|---|---|---|
| POST | `/api/auth/register/` | Create a validated user (implemented) | Public |
| POST | `/api/auth/token/` | Obtain access and refresh tokens (implemented) | Public |
| POST | `/api/auth/token/refresh/` | Refresh an access token (implemented) | Refresh token |
| POST | `/api/auth/token/verify/` | Verify a token (implemented) | Token in request body |
| GET | `/api/todos/` | List the current user's todos (implemented) | Access token |
| POST | `/api/todos/` | Create an owned todo (implemented) | Access token |
| GET | `/api/todos/{id}/` | Read one owned todo (implemented) | Access token |
| PATCH | `/api/todos/{id}/` | Edit or toggle one owned todo (implemented) | Access token |
| DELETE | `/api/todos/{id}/` | Delete one owned todo (implemented) | Access token |

## Authentication flow

1. The Next.js signup form sends registration data to Django, which validates and creates the user.
2. The Next.js login form sends credentials to the token endpoint.
3. Django returns a five-minute access token and a one-day refresh token.
4. The learning frontend stores both tokens in local storage and adds the access token to API requests.
5. Django permissions and queryset filtering enforce ownership; the client-side route guard is only a user-experience feature.
6. Frontend logout clears stored tokens. Server-side refresh-token blacklisting is not implemented.
7. The refresh endpoint exists, but automatic frontend refresh and request retry remain planned.

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
