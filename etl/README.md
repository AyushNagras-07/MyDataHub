# ETL Pipeline

Batch ETL pipeline that reads daily-log JSON files, validates and normalizes them, and loads them into PostgreSQL — with per-file error tracking and a per-run audit trail. See the [root README](../README.md) for how this fits into the wider project.

## Layout

```
etl/
├── config/
│   ├── settings.py          # Folder paths, USER_ID, retry configuration
│   └── logging_config.py    # logging.basicConfig setup (console, INFO level)
├── data/
│   ├── raw/                 # Pipeline input — JSON files to process
│   ├── processed/           # Files that completed all four stages successfully
│   └── failed/              # Files that failed extraction, validation, transform, or load
├── extract/                 # See extract/README.md
├── transform/                # See transform/README.md
├── validation/                # See validation/README.md
├── load/                      # See load/README.md
├── utils/                      # See utils/README.md
└── pipeline.py                 # Orchestrator — entry point for a batch run
```

## Why raw / processed / failed folders

Separating input files by outcome makes the pipeline **idempotent and re-runnable by inspection**: `raw/` only ever contains files that haven't been attempted yet (or need to be retried), `processed/` is a record of what has already been loaded, and `failed/` isolates bad input for manual review without blocking the rest of the batch. `run_pipeline()` in `pipeline.py` moves a file the moment it finishes processing, so a crash mid-batch never leaves an ambiguous state for files already handled.

## Pipeline Orchestration (`pipeline.py`)

`run_pipeline()`:

1. Calls `create_pipeline_run()` to insert a `pipeline_runs` row (`status="RUNNING"`) and get a `pipeline_run_id`.
2. Globs `*.json` in `RAW_FOLDER`, sorted by filename.
3. Calls `process_file(file_path, pipeline_run_id)` for each file, moving it to `PROCESSED_FOLDER` or `FAILED_FOLDER` based on the result.
4. Computes `total_files`, `successful_files`, `failed_files`, `success_rate`, and `execution_time`, derives an overall `status`, logs a summary block, and calls `complete_pipeline_run()` to update the `pipeline_runs` row.

Overall run status logic:

| Condition | Status |
|---|---|
| `failed_files == 0` | `SUCCESS` |
| `failed_files > 0` and `successful_files > 0` | `PARTIAL_SUCCESS` |
| `successful_files == 0` and `failed_files > 0` | `FAILED` |

Note: a run over an empty `raw/` folder (zero files) also reports `SUCCESS`, since `failed_files == 0` in that case too.

`process_file()` tracks which of the four stages (`EXTRACT`, `VALIDATION`, `TRANSFORMATION`, `LOAD`) is active via a local `stage` variable, so any exception can be attributed to the right stage when it's recorded in `pipeline_errors`. A validation failure is handled explicitly (no exception is raised — `validate_daily_data()` returns `(False, errors)`); everything else is caught by a single `try/except` around the remaining stages.

## Configuration (`config/`)

`settings.py` defines:

- `RAW_FOLDER`, `PROCESSED_FOLDER`, `FAILED_FOLDER` — resolved relative to `etl/data/`.
- `USER_ID = 1` — hardcoded. The pipeline currently loads every file under a single user; there is no multi-user ingestion logic despite `users` being a normal table with its own primary key.
- `MAX_RETRY_ATTEMPTS = 3`, `RETRY_DELAY = 2` — passed into `retry_operation()` for the load stage (see [utils/README.md](./utils/README.md)).

`logging_config.py` calls `logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")`. All log output goes to the console; there is no file handler, log rotation, or structured (JSON) logging configured.

## Related Documentation

- [Extraction](./extract/README.md)
- [Validation](./validation/README.md)
- [Transformation](./transform/README.md)
- [Load](./load/README.md)
- [Utils](./utils/README.md)
- [Database schema](../sql/schema/README.md)
- [Testing](../tests/README.md)
