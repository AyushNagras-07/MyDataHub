from etl.extract import daily_input
import re


def _is_number(n):
    return isinstance(n, (int, float))


def validate_daily_data(data):
    errors = []

    log_date = data.get("log_date")

    if log_date is None or not re.match(r"^\d{4}-\d{2}-\d{2}$", log_date):
        errors.append("not proper date format it should be yyyy-mm-dd")

    # personal.mood: 1-5 (scale)
    mood = data.get("personal", {}).get("mood")
    if mood is not None:
        if not _is_number(mood) or not 1 <= mood <= 5:
            errors.append(f"personal.mood must be between 1 and 5, got {mood}")

    # office.hours_worked: 0-24
    hours_worked = data.get("office", {}).get("hours_worked")
    if hours_worked is not None:
        if not _is_number(hours_worked) or not 0 <= hours_worked <= 24:
            errors.append(f"office.hours_worked must be between 0 and 24, got {hours_worked}")

    # learning.study_hours: non-negative and realistic (<=24)
    study_hours = data.get("learning", {}).get("study_hours")
    if study_hours is not None:
        if not _is_number(study_hours) or not 0 <= study_hours <= 24:
            errors.append(f"learning.study_hours must be between 0 and 24, got {study_hours}")

    # finance
    daily_expense = data.get("finance", {}).get("daily_expense")
    if daily_expense is not None:
        if not _is_number(daily_expense) or daily_expense < 0:
            errors.append(f"finance.daily_expense cannot be negative, got {daily_expense}")

    income_received = data.get("finance", {}).get("income_received")
    if income_received is not None:
        if not _is_number(income_received) or income_received < 0:
            errors.append(f"money can't receive negative money sorry - {income_received}")

    # food
    tea_coffee_count = data.get("food", {}).get("tea_coffee_count")
    if tea_coffee_count is not None:
        if not _is_number(tea_coffee_count) or tea_coffee_count < 0 or tea_coffee_count > 50:
            errors.append(f"food.tea_coffee_count must be between 0 and 50, got {tea_coffee_count}")

    # habits
    pushups = data.get("habits", {}).get("pushups")
    if pushups is not None:
        if not _is_number(pushups) or pushups < 0 or pushups > 1000:
            errors.append(f"habits.pushups must be between 0 and 1000, got {pushups}")

    reading_pages = data.get("habits", {}).get("reading_pages")
    if reading_pages is not None:
        if not _is_number(reading_pages) or reading_pages < 0 or reading_pages > 10000:
            errors.append(f"You can not read that much pages in one day - {reading_pages}")

    return len(errors) == 0, errors


# if __name__ == "__main__":
#     file_path = "/home/ayush/MyDataHub/etl/data/raw/2026-08-13.json"
#     result = validate_daily_data(file_path)
#     print("Validation passed" if result else "Validation failed")