CREATE OR REPLACE VIEW monthly_summary AS
SELECT
    DATE_TRUNC('month', log_date)::date AS month_start,

    COUNT(*) AS days_logged,

    -- Office
    COALESCE(SUM(hours_worked), 0) AS total_office_hours,
    ROUND(AVG(hours_worked), 2) AS avg_office_hours,

    -- Learning
    COALESCE(SUM(study_hours), 0) AS total_study_hours,
    ROUND(AVG(study_hours), 2) AS avg_study_hours,

    -- Mood
    ROUND(AVG(mood), 2) AS avg_mood,

    -- Finance
    COALESCE(SUM(daily_expense), 0) AS total_expense,
    COALESCE(SUM(income_received), 0) AS total_income,

    -- Food
    COALESCE(SUM(tea_coffee_count), 0) AS total_tea_coffee,
    ROUND(AVG(tea_coffee_count), 2) AS avg_tea_coffee,

    -- Exercise
    COALESCE(SUM(pushups), 0) AS total_pushups,

    SUM(
        CASE
            WHEN exercise_done = TRUE THEN 1
            ELSE 0
        END
    ) AS exercise_days,

    -- Habits
    SUM(
        CASE
            WHEN bath_taken = TRUE THEN 1
            ELSE 0
        END
    ) AS bath_days,

    SUM(
        CASE
            WHEN hair_washed = TRUE THEN 1
            ELSE 0
        END
    ) AS hair_wash_days,

    SUM(
        CASE
            WHEN hair_oil_applied = TRUE THEN 1
            ELSE 0
        END
    ) AS hair_oil_days,

    -- Reading
    COALESCE(SUM(reading_pages), 0) AS total_reading_pages

FROM daily_summary

GROUP BY DATE_TRUNC('month', log_date)::date;