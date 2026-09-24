# Utils

Two small, single-purpose helpers used by `pipeline.py`.

## `retry.py`

`retry_operation(operation, max_attempts=3, delay=2)` calls `operation()` (a zero-argument callable) and retries on any `Exception`, with exponential backoff between attempts:

```
wait_time = delay * (2 ** (attempt - 1))
```

With the defaults used in `etl/config/settings.py` (`MAX_RETRY_ATTEMPTS=3`, `RETRY_DELAY=2`), a failing operation is attempted 3 times total, waiting 2s after the first failure and 4s after the second, before the original exception is re-raised on the third.

In the pipeline, this wraps **only the load stage** (`load_operation()` in `pipeline.py`'s `process_file()`), since load is the step most likely to fail transiently (database connectivity) rather than deterministically (extract/validate/transform failures won't succeed on a second attempt with the same input).

## `file_handler.py`

`move_file(file_path, destination_folder)` creates the destination folder if it doesn't exist (`os.makedirs(..., exist_ok=True)`) and moves the file into it with `shutil.move`. Used by `pipeline.py` to route a file to `etl/data/processed/` or `etl/data/failed/` once `process_file()` returns.
