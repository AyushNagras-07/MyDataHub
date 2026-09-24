# Extract

Reads a single input file for the pipeline. This is the `EXTRACT` stage referenced throughout `pipeline.py` and the `pipeline_errors.stage` values.

## `daily_input.py`

`extract_daily_data(file_path)` opens the given path as UTF-8 and parses it as JSON:

```python
def extract_daily_data(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)
```

Failure handling is deliberately narrow and re-raises with context instead of swallowing the error:

| Input condition | Behavior |
|---|---|
| File does not exist | Re-raises as `FileNotFoundError(f"Input file not found: {file_path}")` |
| File is not valid JSON | Re-raises as `ValueError(f"Invalid JSON format in file: {file_path}")` |
| File exists and is valid JSON | Returns the parsed object (a `dict` for every real input file in `etl/data/`) |

Both exception types are caught by `process_file()`'s outer `try/except`, so an extraction failure is recorded in `pipeline_errors` with `stage="EXTRACT"` and `error_type` set to the exception's class name (`FileNotFoundError` or `ValueError`), and the file is moved to `etl/data/failed/`.

There is no schema validation at this stage — that happens next, in [validation](../validation/README.md). Extraction only guarantees the file is readable, valid JSON.
