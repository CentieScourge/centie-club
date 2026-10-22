# Notes from Raushan K. (Dev, 43758)

## My part (Dev)

- Dockerfile + docker-compose.yml: one-command local start of the stack (web + PostgreSQL).
- docker-entrypoint.sh: waits for DB, runs migrations and collectstatic on container start.
- GitHub Actions CI: `manage.py check`, migrations check, tests, Docker image build on every PR.
- Smoke tests (`portal/tests.py`): public pages respond 200, admin and login pages are reachable.
- CONTRIBUTING.md: branch/PR workflow for the team.

## How to run locally

```bash
cp .env.example .env        # set DB_HOST=db, DEBUG=True
docker compose up -d --build
docker compose exec web python manage.py createsuperuser
# open http://localhost:8000  and  http://localhost:8000/admin/
```

## How to run tests

```bash
python manage.py test        # needs PostgreSQL reachable per .env
# or inside Docker:
docker compose exec web python manage.py test
```

## Backlog

- Enable `map/` page (route is commented out in `portal/urls.py`).
- Add HTTPS (certbot) to nginx config.
- Add more unit tests for models and forms.
