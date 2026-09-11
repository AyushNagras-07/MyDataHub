def transform_daily_data(data):
    if not isinstance(data, dict):
        raise TypeError(
            "Transformation input must be a dictionary"
        )

    return {
        "log_date":data.get("log_date",{}),
        "personal": data.get("personal", {}),
        "office": data.get("office", {}),
        "learning": data.get("learning", {}),
        "finance": data.get("finance", {}),
        "food": data.get("food", {}),
        "habits": data.get("habits", {})
    }