# Load

Writes transformed data into PostgreSQL and maintains the pipeline audit trail. This is the `LOAD` stage in `pipeline.py`.

## `postgres_loader.py`

`get_connection()` loads `.env` from the repository root via `python-dotenv` and opens a `psycopg2` connection using `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`.

`load_daily_data(data, user_id)` is the entry point called from `pipeline.py`. It performs **one transaction** across seven inserts:

1. `load_daily_log()` — upserts `daily_logs` on `(user_id, log_date)`; on conflict, only `updated_at` is refreshed. Returns the `daily_log_id`.
2. `load_personal_log()`, `load_office_log()`, `load_learning_log()`, `load_finance_log()`, `load_food_log()`, `load_habit_log()` — each upserts its topic table on `daily_log_id`, overwriting every column with `EXCLUDED.*` on conflict.

All seven statements share one `connection`/`cursor`. `connection.commit()` is only called after all seven succeed. If any statement raises, the `except` block calls `connection.rollback()` (undoing the whole batch, including the `daily_logs` upsert) and re-raises — so a day is never left in a state where `daily_logs` exists but some of its topic rows don't. The `finally` block always closes the cursor and connection, whether the transaction succeeded or failed.

A `current_table` variable is updated before each insert purely so the `except` block's log line can report which table was being written when the failure happened — it does not affect control flow.

## `pipeline_run_loader.py`

Three functions, each opening and closing **its own connection** — independent of `load_daily_data()`'s transaction:

| Function | Called from | Effect |
|---|---|---|
| `create_pipeline_run()` | `pipeline.run_pipeline()`, once per batch | Inserts a `pipeline_runs` row with `status="RUNNING"`, commits, returns the new `id` |
| `record_pipeline_error(pipeline_run_id, file_name, stage, error_type, error_message)` | `pipeline.process_file()`, on any per-file failure | Inserts a `pipeline_errors` row |
| `complete_pipeline_run(pipeline_run_id, total_files, successful_files, failed_files, execution_time, status)` | `pipeline.run_pipeline()`, once at the end of the batch | Updates the `pipeline_runs` row with final counts and status |

**Why separate connections/transactions:** if a file's data load fails and rolls back, that rollback must not also erase the fact that it failed. Keeping pipeline-audit writes on their own connections means `pipeline_runs`/`pipeline_errors` always reflect what actually happened, regardless of what the data-loading transaction did.

Each of these three functions also wraps its own `execute` in try/rollback/re-raise/finally-close — so a failure to *record* an error (e.g. the audit database being unreachable) doesn't leave a dangling connection, though it does mean that failure would itself propagate up uncaught (there's no fallback logging path if writing to `pipeline_errors` fails).
