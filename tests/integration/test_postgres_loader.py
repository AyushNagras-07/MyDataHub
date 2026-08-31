from etl.load.postgres_loader import load_daily_log ,load_daily_data
from datetime import date
import psycopg2


def test_database_connection(db_connection):

    cursor = db_connection.cursor()

    cursor.execute("SELECT current_database();")

    result = cursor.fetchone()

    cursor.close()

    assert result == ("mydatahub_test",)


def test_daily_log_insert(db_connection):

    cursor = db_connection.cursor()

    # Create test user
    cursor.execute(
        """
        INSERT INTO users (name, email)
        VALUES (%s, %s)
        RETURNING id;
        """,
        ("Test User", "integration_test@example.com")
    )

    user_id = cursor.fetchone()[0]

    data = {
        "log_date": "2026-08-27"
    }

    # Use the REAL loader
    daily_log_id = load_daily_log(
        cursor,
        data,
        user_id
    )

    # Verify directly in PostgreSQL
    cursor.execute(
        """
        SELECT user_id, log_date
        FROM daily_logs
        WHERE id = %s;
        """,
        (daily_log_id,)
    )

    result = cursor.fetchone()

    assert result == (
        user_id,
        date(2026, 8, 27)
    )

    cursor.close()

def test_daily_log_upsert(db_connection):

    cursor = db_connection.cursor()

    # Create test user
    cursor.execute(
        """
        INSERT INTO users (name, email)
        VALUES (%s, %s)
        RETURNING id;
        """,
        ("Upsert Test User", "upsert_test@example.com")
    )

    user_id = cursor.fetchone()[0]

    # First load
    data = {
        "log_date": "2026-08-28"
    }

    first_id = load_daily_log(
        cursor,
        data,
        user_id
    )

    # Second load - same user + same date
    second_id = load_daily_log(
        cursor,
        data,
        user_id
    )

    # Both operations should point to the same daily log
    assert first_id == second_id

    # Verify only ONE record exists
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM daily_logs
        WHERE user_id = %s
          AND log_date = %s;
        """,
        (user_id, "2026-08-28")
    )

    count = cursor.fetchone()[0]

    assert count == 1

    cursor.close()



def test_load_rollback_on_database_error(db_connection):

    cursor = db_connection.cursor()

    # Create test user
    cursor.execute(
        """
        INSERT INTO users (name, email)
        VALUES (%s, %s)
        RETURNING id;
        """,
        ("Rollback Test User", "rollback_test12@example.com")
    )

    user_id = cursor.fetchone()[0]

    db_connection.commit()

    # Invalid mood: PostgreSQL allows the transaction
    # to reach the database, but the CHECK constraint fails.
    data = {
        "log_date": "2026-08-29",

        "personal": {
            "wake_up_time": "07:30",
            "sleep_time": "23:15",
            "mood": 9,
            "special_note": "This should fail"
        }
    }

    # The loader should fail and rollback.
    try:
        load_daily_data(data, user_id)
    except psycopg2.errors.CheckViolation:
        pass

    # Verify the daily_logs row was NOT left behind.
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM daily_logs
        WHERE user_id = %s
          AND log_date = %s;
        """,
        (user_id, "2026-08-29")
    )

    count = cursor.fetchone()[0]

    assert count == 0

    # Cleanup test user
    cursor.execute(
        """
        DELETE FROM users
        WHERE id = %s;
        """,
        (user_id,)
    )

    db_connection.commit()

    cursor.close()