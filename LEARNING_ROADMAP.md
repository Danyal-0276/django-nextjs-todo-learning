# Full-stack Todo learning roadmap

Work through these steps in order and commit after each working milestone. Commands assume Windows PowerShell, the repository root, and an activated `venv`. Examples are illustrative—adapt names after reading the relevant documentation.

## 1. Understand the existing Django project

- **Learn:** request → URL → view → model → template flow; sessions and migrations.
- **Why:** API work is easier when you can trace the current server-rendered flow.
- **Files later:** `todo/todo/urls.py`, `views.py`, `models.py`, templates.
- **Commands:** `cd todo`; `python manage.py check`; `python manage.py show_urls` only if you later install a package that provides it.
- **Example:** trace `path("todopage/", views.todo)` into the `todo` view and its database query.
- **Test:** run the server and manually map every screen to a URL and view.
- **Avoid:** changing several layers before understanding which one owns each behavior.

## 2. Refine the Todo model

- **Learn:** fields, defaults, choices, ownership, and model validation.
- **Why:** the API contract will be built around this data.
- **Files later:** `todo/todo/models.py`, a new migration.
- **Commands:** `python manage.py makemigrations`; `python manage.py migrate`.
- **Example:** `completed = models.BooleanField(default=False)` and optionally `updated_at = models.DateTimeField(auto_now=True)`.
- **Test:** create and toggle a record in `python manage.py shell` or admin.
- **Avoid:** editing old migration files after they have been applied.

## 3. Configure PostgreSQL in Django

- **Learn:** database drivers, connection settings, environment variables, roles, and databases.
- **Why:** PostgreSQL matches common production deployments and teaches real database configuration.
- **Files later:** `settings.py`, root `.env` (untracked), dependency file.
- **Commands:** `pip install psycopg[binary] python-dotenv`; create the database/user with pgAdmin or `psql`; then `python manage.py migrate`.
- **Example:** `DATABASES["default"] = {"ENGINE": "django.db.backends.postgresql", "NAME": os.getenv("POSTGRES_DB"), ...}`.
- **Test:** `python manage.py dbshell` and `python manage.py migrate` connect successfully.
- **Avoid:** committing passwords, pointing tests at valuable data, or assuming SQLite data moves automatically.

## 4. Create and apply migrations

- **Learn:** schema history, migration review, and rollback basics.
- **Why:** model code does not alter the database until migrations run.
- **Files later:** `todo/todo/migrations/*.py`.
- **Commands:** `python manage.py makemigrations`; `python manage.py sqlmigrate todo 0002`; `python manage.py migrate`.
- **Example:** inspect generated SQL before applying it.
- **Test:** `python manage.py showmigrations` shows `[X]` and admin exposes new fields.
- **Avoid:** deleting migration history to solve ordinary conflicts.

## 5. Install and configure Django REST Framework

- **Learn:** parsers, renderers, authentication, and DRF settings.
- **Why:** DRF turns model behavior into consistent HTTP APIs.
- **Files later:** `settings.py`, dependency file.
- **Commands:** `pip install djangorestframework`; add `rest_framework` to `INSTALLED_APPS`.
- **Example:** `REST_FRAMEWORK = {"DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"]}`.
- **Test:** `python manage.py check` and confirm DRF imports in the shell.
- **Avoid:** making every endpoint public while experimenting.

## 6. Create serializers

- **Learn:** input validation, output representation, read-only fields, and `create`/`update`.
- **Why:** serializers define the boundary between JSON and Django objects.
- **Files later:** new `todo/todo/serializers.py`.
- **Commands:** no special command; run tests after editing.
- **Example:** `class TodoSerializer(serializers.ModelSerializer): class Meta: model=Todo; fields=("srno","title","completed","date")`.
- **Test:** instantiate with valid/invalid payloads in the shell and inspect `.errors`.
- **Avoid:** accepting a client-provided `user`; assign ownership from `request.user`.

## 7. Create views or viewsets

- **Learn:** generic views versus `ModelViewSet`, querysets, and hooks.
- **Why:** views map HTTP methods to CRUD behavior.
- **Files later:** a new `api_views.py` or carefully separated additions to `views.py`.
- **Commands:** `python manage.py test`.
- **Example:** override `get_queryset()` to return `Todo.objects.filter(user=self.request.user)` and `perform_create()` to save the current user.
- **Test:** authenticated users can CRUD their own records.
- **Avoid:** `Todo.objects.all()` on a user-owned endpoint.

## 8. Configure API URLs and routers

- **Learn:** URL namespaces, routers, basenames, and trailing slashes.
- **Why:** predictable endpoints simplify frontend integration.
- **Files later:** new `api_urls.py`, existing project `urls.py`.
- **Commands:** `python manage.py check`; run the server.
- **Example:** `router.register("todos", TodoViewSet, basename="todo")`; include it under `path("api/", include(...))`.
- **Test:** visit DRF's browsable API or inspect registered routes.
- **Avoid:** mixing page and API route names without a namespace.

## 9. Test CRUD endpoints using Postman

- **Learn:** HTTP verbs, JSON bodies, headers, status codes, and collections.
- **Why:** isolating the API prevents frontend bugs from hiding backend bugs.
- **Files later:** optional exported `docs/postman_collection.json` without secrets.
- **Commands:** run `python manage.py runserver`; send GET/POST/PATCH/DELETE requests.
- **Example:** POST `{"title":"Learn serializers"}` with `Content-Type: application/json`.
- **Test:** expect 201, 200, and 204 where appropriate; verify database changes.
- **Avoid:** treating only a 200 response as success or storing real tokens in committed collections.

## 10. Add user registration

- **Learn:** password hashing, unique constraints, serializer validation, and safe response fields.
- **Why:** frontend users need an API-native account flow.
- **Files later:** auth serializer/view and API URL files.
- **Commands:** `python manage.py test`.
- **Example:** call `User.objects.create_user(...)`; never assign a raw password to `user.password`.
- **Test:** duplicate username/email errors are clear and passwords are hashed.
- **Avoid:** returning password fields or leaking which sensitive credentials exist.

## 11. Add JWT authentication using Simple JWT

- **Learn:** signed tokens, claims, expiry, access versus refresh tokens.
- **Why:** the separate Next.js application needs an API authentication mechanism.
- **Files later:** `settings.py`, API URLs, dependencies.
- **Commands:** `pip install djangorestframework-simplejwt`; add token views to URLs.
- **Example:** configure DRF's JWT authentication class and `TokenObtainPairView`.
- **Test:** obtain a pair, send `Authorization: Bearer <access>`, and confirm an invalid token gets 401.
- **Avoid:** long-lived access tokens, secrets in Git, or logging complete tokens.

## 12. Add refresh-token handling

- **Learn:** expiry detection, rotation, blacklisting, and retry limits.
- **Why:** short access-token life should not force constant logins.
- **Files later:** Django JWT settings; `frontend/src/lib/api-client.ts`; `token-storage.ts`.
- **Commands:** optionally install/configure Simple JWT's blacklist app, then migrate.
- **Example:** on one 401, POST the refresh token, save the returned access token, retry once.
- **Test:** use a short expiry locally and verify refresh succeeds; invalid refresh logs out.
- **Avoid:** recursive retry loops or sending refresh tokens on every API request.

## 13. Add permissions and authorization

- **Learn:** authentication versus authorization and object-level permissions.
- **Why:** being logged in must not permit access to another user's data.
- **Files later:** API views plus optional `permissions.py`.
- **Commands:** `python manage.py test`.
- **Example:** both filter the queryset by owner and reject objects not owned by `request.user`.
- **Test:** create two users; user B must receive 404/403 for user A's todo IDs.
- **Avoid:** relying on hidden frontend buttons for security.

## 14. Ensure users access only their own todos

- **Learn:** multi-user test design and information leakage.
- **Why:** ownership is the core security rule for this app.
- **Files later:** viewset tests and queryset logic.
- **Commands:** `python manage.py test todo`.
- **Example:** assert list responses contain only the authenticated user's records.
- **Test:** cover list, retrieve, update, toggle, and delete across two users.
- **Avoid:** testing only list filtering while detail routes remain exposed.

## 15. Configure CORS

- **Learn:** browser origins, preflight requests, allowed headers, and credentials.
- **Why:** localhost ports 3000 and 8000 are different origins.
- **Files later:** `settings.py`, middleware list, environment variables.
- **Commands:** `pip install django-cors-headers`.
- **Example:** allow exactly `http://localhost:3000` during development.
- **Test:** make a browser request and inspect its preflight/response headers.
- **Avoid:** `CORS_ALLOW_ALL_ORIGINS=True` in production.

## 16. Connect Next.js to Django

- **Learn:** client/server components, async requests, base URLs, and network debugging.
- **Why:** this is the first end-to-end milestone.
- **Files later:** frontend services, hooks, forms, `.env.local`.
- **Commands:** run Django and `npm run dev` in separate terminals.
- **Example:** replace the hook's initial mock list with `await todoService.list()`.
- **Test:** browser DevTools shows a successful request and the UI renders database data.
- **Avoid:** hardcoding the backend URL throughout components.

## 17. Replace mock services with real requests

- **Learn:** data fetching, optimistic updates, rollbacks, and request state.
- **Why:** UI operations must now reflect server truth.
- **Files later:** `frontend/src/hooks/use-todos.ts`, auth forms/services.
- **Commands:** `npm run lint`; `npm run build`.
- **Example:** create through `todoService.create`, then add the returned server object to state.
- **Test:** refresh keeps todos because they now live in PostgreSQL.
- **Avoid:** inventing client IDs once the server generates them or ignoring failed writes.

## 18. Store and send tokens safely

- **Learn:** XSS, CSRF, localStorage tradeoffs, HttpOnly cookies, and HTTPS.
- **Why:** token storage determines the impact of browser attacks.
- **Files later:** token helper/API client or a Backend-for-Frontend cookie route.
- **Commands:** no universal command; document and test the chosen architecture.
- **Example:** the existing helper demonstrates localStorage but explicitly does not claim production safety.
- **Test:** protected requests include the access token; logout clears credentials; refresh expiry ends the session.
- **Avoid:** committing tokens, exposing secrets via `NEXT_PUBLIC_*`, or claiming JWT alone makes an app secure.

## 19. Handle validation and API errors

- **Learn:** DRF error shapes, field errors, network failures, 401/403/404 differences.
- **Why:** users need actionable feedback and the UI must remain consistent.
- **Files later:** serializers, API client, forms, todo hook/components.
- **Commands:** run backend and frontend tests/lint.
- **Example:** map `{title:["This field may not be blank."]}` to the title control.
- **Test:** deliberately submit invalid data, stop Django, expire a token, and retry actions.
- **Avoid:** showing only “Something went wrong” or leaving optimistic changes after failure.

## 20. Add testing and deployment

- **Learn:** Django `TestCase`/API tests, React testing, end-to-end flows, CI, environment separation, HTTPS, static files, and hosted databases.
- **Why:** automated verification makes future changes safe and deployment repeatable.
- **Files later:** backend `tests/`, frontend test files, CI workflow, production settings.
- **Commands:** `python manage.py test`; `npm run lint`; `npm run build`; later add a frontend test runner.
- **Example:** CI should install each side independently, run checks, and never print secrets.
- **Test:** deploy to a staging environment and complete register → login → CRUD → refresh → logout.
- **Avoid:** deploying with `DEBUG=True`, SQLite, empty `ALLOWED_HOSTS`, development email, or HTTP-only traffic.

## Recommended first task

Start with steps 1–2: fix the legacy login-name collision, add a real `completed` field through a new migration, and write tests that prove users cannot edit or delete another user's todo. That foundation will make the later API safer and easier to understand.
