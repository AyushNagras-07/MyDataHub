from unittest.mock import MagicMock, patch

from etl.load.postgres_loader import load_daily_log ,load_personal_log ,load_daily_data

def test_load_daily_log():

    cursor = MagicMock()

    cursor.fetchone.return_value = (10,)

    data = {
        "log_date": "2026-08-26"
    }

    result = load_daily_log(
        cursor,
        data,
        user_id=1
    )

    assert result == 10
    cursor.execute.assert_called_once()
def test_load_daily_log_parameters():

    cursor = MagicMock()

    cursor.fetchone.return_value = (15,)

    data = {
        "log_date": "2026-08-26"
    }

    result = load_daily_log(
        cursor,
        data,
        user_id=1
    )

    assert result == 15

    cursor.execute.assert_called_once()

    sql, parameters = cursor.execute.call_args.args

    assert parameters == (1, "2026-08-26")

def test_load_daily_log_returns_database_id():

    cursor = MagicMock()

    cursor.fetchone.return_value = (42,)

    data = {
        "log_date": "2026-08-26"
    }

    result = load_daily_log(
        cursor,
        data,
        user_id=1
    )

    assert result == 42

def test_load_personal_log():

    cursor = MagicMock()

    data = {
        "personal": {
            "wake_up_time": "07:30",
            "sleep_time": "23:15",
            "mood": 4,
            "special_note": "Good productive day"
        }
    }

    load_personal_log(
        cursor,
        daily_log_id=10,
        data=data
    )

    cursor.execute.assert_called_once()

    sql, parameters = cursor.execute.call_args.args

    assert parameters == (
        10,
        "07:30",
        "23:15",
        4,
        "Good productive day"
    )



def test_load_daily_data_rolls_back_on_failure():

    connection = MagicMock()
    cursor = connection.cursor.return_value

    # Make the database operation fail
    cursor.execute.side_effect = Exception("Database failure")

    data = {
        "log_date": "2026-08-26",
        "personal": {
            "mood": 4
        }
    }

    with patch(
        "etl.load.postgres_loader.get_connection",
        return_value=connection
    ):

        try:
            load_daily_data(data, user_id=1)
        except Exception:
            pass

    connection.rollback.assert_called_once()