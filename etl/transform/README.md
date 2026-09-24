# Transform

Structural normalization step between validation and load. This is the `TRANSFORMATION` stage in `pipeline.py`.

## `daily_transform.py`

`transform_daily_data(data)` takes the parsed, already-validated JSON `dict` and rebuilds it with every expected top-level key present, defaulting missing sections to an empty dict:

```python
{
    "log_date": data.get("log_date", {}),
    "personal": data.get("personal", {}),
    "office": data.get("office", {}),
    "learning": data.get("learning", {}),
    "finance": data.get("finance", {}),
    "food": data.get("food", {}),
    "habits": data.get("habits", {})
}
```

This does **not** perform type coercion, unit conversion, or derived-field calculation — it only guarantees shape. That guarantee is what lets every `load_*_log()` function in [postgres_loader.py](../load/README.md) call `.get()` on a section without a `KeyError`, even when an input file omits a whole section (e.g. no `finance` block on a day with no spending).

`data.get("log_date", {})` defaults to `{}` rather than `None` if `log_date` is absent — in practice this case never reaches transformation, since `validate_daily_data()` already requires `log_date` to match `^\d{4}-\d{2}-\d{2}$` and rejects the file otherwise.

Input other than a `dict` raises `TypeError("Transformation input must be a dictionary")`, which is caught and recorded the same way as any other `TRANSFORMATION`-stage failure.
