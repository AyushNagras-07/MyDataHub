from etl.validation.daily_validation import validate_daily_data


def test_valid_daily_data():

    data = {
        "log_date": "2026-08-09",

        "personal": {
            "mood": 3
        },

        "office": {
            "hours_worked": 8
        },

        "learning": {
            "study_hours": 2
        },

        "finance": {
            "daily_expense": 200,
            "income_received": 0
        },

        "food": {
            "tea_coffee_count": 2
        },

        "habits": {
            "pushups": 30,
            "reading_pages": 10
        }
    }

    assert validate_daily_data(data) is True

def test_invalid_mood():

    data1 = {
    "log_date": "2026-08-09",

        "personal": {
            "mood": 9
        }
    }

    assert validate_daily_data(data1) is False

def test_negative_expense():

    data = {
        "log_date": "2026-08-09",

        "finance": {
            "daily_expense": -100
        }
    }

    assert validate_daily_data(data) is False