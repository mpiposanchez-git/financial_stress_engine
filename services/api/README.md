# API Service (`services/api`)

FastAPI service for cloud deployment requirements in `docs/system_architecture_instructions.md` (PART VII).

## Run locally

From repository root:

```bash
uv run uvicorn services.api.app.main:app --reload --port 8000
```

## Tests (service scope)

```bash
uv run pytest services/api/tests -v
```

## Lint

```bash
uv run ruff check services/api
```

## Render compatibility

Use this start command in Render:

```bash
uv run uvicorn services.api.app.main:app --host 0.0.0.0 --port $PORT
```
