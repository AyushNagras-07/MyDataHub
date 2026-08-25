from etl.extract import daily_input
import re


def _is_number(n):
    return isinstance(n, (int, float))


def validate_daily_data(data):

    log_date = data.get("log_date")

    if log_date is None or not re.match(r"^\d{4}-\d{2}-\d{2}$", log_date):
        return False

    # personal.mood: 1-5 (scale)
    mood = data.get("personal", {}).get("mood")
    if mood is not None:
        if not _is_number(mood) or not 1 <= mood <= 5:
            print(f"Your mood score should be between 1 to 5 but your is {mood}")
            return False

    # office.hours_worked: 0-24
    hours_worked = data.get("office", {}).get("hours_worked")
    if hours_worked is not None:
        if not _is_number(hours_worked) or not 0 <= hours_worked <= 24:
            print(f"sorry you can not work more than 24 hours a day {hours_worked}")
            return False

    # learning.study_hours: non-negative and realistic (<=24)
    study_hours = data.get("learning", {}).get("study_hours")
    if study_hours is not None:
        if not _is_number(study_hours) or not 0 <= study_hours <= 24:
            print(f"sorry you can not stidy more than 24 hours a day {study_hours}")
            return False

    # finance
    daily_expense = data.get("finance", {}).get("daily_expense")
    if daily_expense is not None:
        if not _is_number(daily_expense) or daily_expense < 0:
            print(f"money can't spend negative money sorry{daily_expense}")
            return False

    income_received = data.get("finance", {}).get("income_received")
    if income_received is not None:
        if not _is_number(income_received) or income_received < 0:
            print(f"money can't receive negative money sorry{income_received}")
            return False

    # food
    tea_coffee_count = data.get("food", {}).get("tea_coffee_count")
    if tea_coffee_count is not None:
        if not _is_number(tea_coffee_count) or tea_coffee_count < 0 or tea_coffee_count > 50:
            print(f"you def didnt drink more than 50 tea and coffee impossible or less than 0 : {tea_coffee_count}")
            return False

    # habits
    pushups = data.get("habits", {}).get("pushups")
    if pushups is not None:
        if not _is_number(pushups) or pushups < 0 or pushups > 1000:
            print(f"more than 1000 push ups impossible {pushups}")
            return False

    reading_pages = data.get("habits", {}).get("reading_pages")
    if reading_pages is not None:
        if not _is_number(reading_pages) or reading_pages < 0 or reading_pages > 10000:
            return False

    return True


if __name__ == "__main__":
    file_path = "/home/ayush/MyDataHub/etl/data/raw/2026-08-13.json"
    result = validate_daily_data(file_path)
    print("Validation passed" if result else "Validation failed")