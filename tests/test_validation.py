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

    valid, errors = validate_daily_data(data)

    assert valid is True
    assert errors == []

def test_invalid_mood():

    data1 = {
    "log_date": "2026-08-09",

        "personal": {
            "mood": 9
        }
    }

    valid, errors = validate_daily_data(data1)

    assert valid is False
    assert len(errors) == 1
    assert "mood" in errors[0]

def test_negative_expense():

    data = {
        "log_date": "2026-08-09",

        "finance": {
            "daily_expense": -100
        }
    }

    valid, errors = validate_daily_data(data)

    assert valid is False
    assert len(errors) == 1
    assert "daily_expense" in errors[0]

def test_multiple_validation_errors():

    data = {
        "log_date": "2026-08-09",

        "personal": {
            "mood": 9
        },

        "office": {
            "hours_worked": 30
        },

        "learning": {
            "study_hours": -5
        },

        "finance": {
            "daily_expense": -100
        }
    }

    valid, errors = validate_daily_data(data)

    assert valid is False
    assert len(errors) == 4