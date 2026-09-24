# Tests

24 tests total, split between fast unit tests (no database) and integration tests (a real Postgres test database). Last recorded run: 24 passed.

## Layout

```
tests/
├── test_validation.py       # 4 tests  — validation rule behavior
├── test_transformation.py   # 2 tests  — transform_daily_data() shape
├── test_retry.py             # 3 tests  — retry_operation() success/backoff/exhaustion
├── test_loader.py             # 5 tests  — postgres_loader functions with a mocked cursor/connection
├── test_pipeline.py           # 4 tests  — process_file()/run_pipeline() with mocked stages + real temp folders
└── integration/
    ├── conftest.py                    # db_connection fixture, loads .env.test
    ├── test_postgres_loader.py         # 4 tests  — real inserts/upserts/rollback against Postgres
    └── test_pipeline_run_loader.py     # 2 tests  — real pipeline_runs inserts/updates against Postgres
```

## Unit Tests

Run against mocked dependencies — no network, no database:

- `test_validation.py` / `test_transformation.py` call the pure functions directly with in-memory `dict`s.
- `test_retry.py` exercises `retry_operation()` with `delay=0` so backoff doesn't slow the suite down, covering first-attempt success, success-after-retry, and exhaustion-after-`max_attempts`.
- `test_loader.py` mocks the `cursor`/`connection` (via `unittest.mock.MagicMock`) to assert the exact SQL parameters passed to `execute()`, and that `load_daily_data()` calls `connection.rollback()` when an insert raises.
- `test_pipeline.py` mocks the extract/validate/transform/retry functions to test `process_file()`'s control flow, and uses `pytest`'s `tmp_path` + `monkeypatch` to point `pipeline.RAW_FOLDER` / `PROCESSED_FOLDER` / `FAILED_FOLDER` at temporary directories, so file-move behavior is tested against the real filesystem without touching `etl/data/`.

## Integration Tests

Require a **live PostgreSQL database with the schema from `sql/schema/` already applied**, and connect using `.env.test` rather than `.env`:

```python
# tests/integration/conftest.py
load_dotenv(".env.test", override=True)
connection = psycopg2.connect(host=..., port=..., database=..., user=..., password=...)
```

`db_connection` is a `pytest` fixture that yields the connection and, on teardown, **rolls back and closes** it — so anything a test writes through this fixture's cursor is discarded automatically. Tests that call the real loader functions (which open their own connections and commit internally, e.g. `load_daily_data()`) create real, committed rows and are responsible for cleaning up after themselves (see `test_load_rollback_on_database_error`, which deletes its own test user at the end).

`test_postgres_loader.py` covers: the fixture connects to the right database, a basic insert through `load_daily_log()`, upsert-returns-the-same-id behavior, and that `load_daily_data()` rolls back and leaves no `daily_logs` row when a `CHECK` constraint (`mood <= 5`) is violated.

`test_pipeline_run_loader.py` covers `create_pipeline_run()` (row created with `status="RUNNING"`) and `complete_pipeline_run()` (row updated with final counts/status).

**Why a separate test database:** integration tests perform real commits (`load_daily_data`, `create_pipeline_run`, etc.). Pointing them at `.env.test` — a different `DB_NAME` — means running the suite can never corrupt or pollute real personal data in the database configured by `.env`.

## Running Tests

```bash
pip install -r requirements.txt

# Unit tests only — no database needed
pytest tests/ --ignore=tests/integration

# Everything, including integration tests
# (requires .env.test pointed at a Postgres database with the schema applied)
pytest
```

There is no `pytest.ini`/`pyproject.toml` in the repository — tests are discovered by `pytest`'s defaults, and `etl`/`tests` are importable because they're resolved relative to the repository root you run `pytest` from.
