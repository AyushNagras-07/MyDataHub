def transform_daily_data(data):

    return {
        "log_date":data.get("log_date",{}),
        "personal": data.get("personal", {}),
        "office": data.get("office", {}),
        "learning": data.get("learning", {}),
        "finance": data.get("finance", {}),
        "food": data.get("food", {}),
        "habits": data.get("habits", {})
    }