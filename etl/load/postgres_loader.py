import psycopg2


def get_connection():
    return psycopg2.connect(
        host="localhost",
        port=5432,
        database="mydatahub",
        user="postgres",
        password="dhoni"
    )

#daily
def load_daily_log(cursor, data, user_id):

    cursor.execute(
        """
        INSERT INTO daily_logs
        (user_id, log_date)
        VALUES (%s, %s)
        RETURNING id;
        """,
        (
            user_id,
            data["log_date"]
        )
    )

    return cursor.fetchone()[0]

#personal
def load_personal_log(cursor, daily_log_id, data):

    personal = data.get("personal", {})

    cursor.execute(
        """
        INSERT INTO personal_logs
        (
            daily_log_id,
            wake_up_time,
            sleep_time,
            mood,
            special_note
        )
        VALUES (%s, %s, %s, %s, %s);
        """,
        (
            daily_log_id,
            personal.get("wake_up_time"),
            personal.get("sleep_time"),
            personal.get("mood"),
            personal.get("special_note")
        )
    )

#office
def load_office_log(cursor, daily_log_id, data):

    office = data.get("office", {})

    cursor.execute(
        """
        INSERT INTO office_logs
        (
            daily_log_id,
            hours_worked,
            main_work_completed,
            office_learnings
        )
        VALUES (%s, %s, %s, %s);
        """,
        (
            daily_log_id,
            office.get("hours_worked"),
            office.get("main_work_completed"),
            office.get("office_learnings")
        )
    )

#learning
def load_learning_log(cursor, daily_log_id, data):

    learning = data.get("learning", {})

    cursor.execute(
        """
        INSERT INTO learning_logs
        (
            daily_log_id,
            topic_learned,
            study_hours,
            project_progress
        )
        VALUES (%s, %s, %s, %s);
        """,
        (
            daily_log_id,
            learning.get("topic_learned"),
            learning.get("study_hours"),
            learning.get("project_progress")
        )
    )

#finance
def load_finance_log(cursor, daily_log_id, data):

    finance = data.get("finance", {})

    cursor.execute(
        """
        INSERT INTO finance_logs
        (
            daily_log_id,
            daily_expense,
            income_received
        )
        VALUES (%s, %s, %s);
        """,
        (
            daily_log_id,
            finance.get("daily_expense"),
            finance.get("income_received")
        )
    )

#Food 
def load_food_log(cursor, daily_log_id, data):

    food = data.get("food", {})

    cursor.execute(
        """
        INSERT INTO food_logs
        (
            daily_log_id,
            breakfast,
            lunch,
            dinner,
            tea_coffee_count
        )
        VALUES (%s, %s, %s, %s, %s);
        """,
        (
            daily_log_id,
            food.get("breakfast"),
            food.get("lunch"),
            food.get("dinner"),
            food.get("tea_coffee_count")
        )
    )

#Habits
def load_habit_log(cursor, daily_log_id, data):

    habits = data.get("habits", {})

    cursor.execute(
        """
        INSERT INTO habit_logs
        (
            daily_log_id,
            bath_taken,
            hair_washed,
            hair_oil_applied,
            exercise_done,
            pushups,
            reading_pages
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s);
        """,
        (
            daily_log_id,
            habits.get("bath_taken", False),
            habits.get("hair_washed", False),
            habits.get("hair_oil_applied", False),
            habits.get("exercise_done", False),
            habits.get("pushups"),
            habits.get("reading_pages")
        )
    )


#main function
def load_daily_data(data, user_id):

    connection = get_connection()

    try:
        cursor = connection.cursor()

        daily_log_id = load_daily_log(
            cursor,
            data,
            user_id
        )

        load_personal_log(
            cursor,
            daily_log_id,
            data
        )

        load_office_log(
            cursor,
            daily_log_id,
            data
        )

        load_learning_log(
            cursor,
            daily_log_id,
            data
        )

        load_finance_log(
            cursor,
            daily_log_id,
            data
        )

        load_food_log(
            cursor,
            daily_log_id,
            data
        )

        load_habit_log(
            cursor,
            daily_log_id,
            data
        )

        connection.commit()

        print(
            f"Daily data loaded successfully. "
            f"daily_log_id={daily_log_id}"
        )

    except Exception as error:

        connection.rollback()

        print("Load failed. Transaction rolled back.")
        print(error)

        raise

    finally:

        cursor.close()
        connection.close()