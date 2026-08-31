from etl.transform.daily_transform import transform_daily_data


def test_transformation_preserves_log_date():

    data = {
        "log_date": "2026-08-09",
        "personal": {
            "mood": 4
        }
    }

    result = transform_daily_data(data)

    assert result["log_date"] == "2026-08-09"

def test_transformation_preserves_sections():

    data = {
        "log_date": "2026-08-09",
        "personal": {"mood": 4},
        "office": {"hours_worked": 8},
        "learning": {"study_hours": 2},
        "finance": {"daily_expense": 200},
        "food": {"tea_coffee_count": 2},
        "habits": {"pushups": 30}
    }

    result = transform_daily_data(data)

    assert "personal" in result
    assert "office" in result
    assert "learning" in result
    assert "finance" in result
    assert "food" in result
    assert "habits" in result