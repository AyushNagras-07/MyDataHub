CREATE OR REPLACE VIEW daily_summary AS
SELECT
    d.id AS daily_log_id,
    d.log_date,

    p.mood,
    p.wake_up_time,
    p.sleep_time,

    o.hours_worked,

    l.study_hours,

    f.daily_expense,
    f.income_received,

    fo.tea_coffee_count,

    h.bath_taken,
    h.hair_washed,
    h.hair_oil_applied,
    h.exercise_done,
    h.pushups,
    h.reading_pages

FROM daily_logs d

LEFT JOIN personal_logs p
    ON d.id = p.daily_log_id

LEFT JOIN office_logs o
    ON d.id = o.daily_log_id

LEFT JOIN learning_logs l
    ON d.id = l.daily_log_id

LEFT JOIN finance_logs f
    ON d.id = f.daily_log_id

LEFT JOIN food_logs fo
    ON d.id = fo.daily_log_id

LEFT JOIN habit_logs h
    ON d.id = h.daily_log_id;