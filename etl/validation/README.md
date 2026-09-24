# Validation

Business-rule validation that runs after extraction and before transformation — the `VALIDATION` stage in `pipeline.py`. This is hand-written range/format checking, not JSON-Schema or a validation library.

## `daily_validation.py`

`validate_daily_data(data)` returns `(is_valid: bool, errors: list[str])`. It never raises — a validation failure is a normal return value, which is why `process_file()` handles it as an explicit `if not valid:` branch rather than via the stage's `try/except`.

Two behaviors worth knowing:

- **Only `log_date` is required to exist.** Every other field is checked with `data.get(...)`, and a missing field is skipped rather than treated as an error — validation only rejects a field that is present and out of range or the wrong type.
- **All violations are collected**, not just the first one. A file with four separate problems produces four separate messages in `errors`.

## Validation Rules

| Field | Rule | Error condition |
|---|---|---|
| `log_date` | Must match `^\d{4}-\d{2}-\d{2}$` | Missing or wrong format |
| `personal.mood` | `1 <= mood <= 5` | Out of range or non-numeric |
| `office.hours_worked` | `0 <= hours_worked <= 24` | Out of range or non-numeric |
| `learning.study_hours` | `0 <= study_hours <= 24` | Out of range or non-numeric |
| `finance.daily_expense` | `>= 0` | Negative |
| `finance.income_received` | `>= 0` | Negative |
| `food.tea_coffee_count` | `0 <= count <= 50` | Out of range or non-numeric |
| `habits.pushups` | `0 <= pushups <= 1000` | Out of range or non-numeric |
| `habits.reading_pages` | `0 <= pages <= 10000` | Out of range or non-numeric |

`_is_number(n)` accepts `int` or `float` (booleans are technically `int` in Python and would pass this check, but no numeric field is fed a boolean in practice).

## Validation vs. Database Constraints

A few application-level thresholds are **stricter or looser** than the corresponding database `CHECK` constraint. Data that passes `validate_daily_data()` can still be rejected by PostgreSQL, and vice versa for fields the validator doesn't check at all:

| Field | Application validation | Database `CHECK` constraint |
|---|---|---|
| `personal.mood` | 1–5 | 1–5 (`chk_personal_logs_mood`) — matches |
| `office.hours_worked` | 0–24 | 0–24 (`chk_hours_worked`) — matches |
| `learning.study_hours` | 0–24 | 0–24 (`chk_study_hours`) — matches |
| `finance.daily_expense` / `income_received` | `>= 0` | `>= 0` (`chk_daily_expense`, `chk_income_received`) — matches |
| `food.tea_coffee_count` | 0–50 | **0–20** (`chk_tea_coffee_count`) — narrower in the database |
| `habits.pushups` | 0–1000 | 0–1000 (`chk_pushups`) — matches |
| `habits.reading_pages` | 0–10000 | **`>= 0`, no upper bound** (`chk_reading_pages`) — database allows more than validation does |

`tests/integration/test_postgres_loader.py::test_load_rollback_on_database_error` calls `load_daily_data()` directly with `mood=9`, bypassing `validate_daily_data()` entirely, to confirm that the database's `CHECK` constraints act as a safety net independent of application validation — PostgreSQL raises `CheckViolation`, and the loader's transaction rolls back cleanly (see [load/README.md](../load/README.md)).
