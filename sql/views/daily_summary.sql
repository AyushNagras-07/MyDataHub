-- ==========================================
-- Indexes for MyDataHub
-- Description: Performance optimization.
-- ==========================================

-------------------------------------------------
-- DAILY LOGS
-------------------------------------------------

CREATE INDEX idx_daily_logs_log_date
ON daily_logs(log_date);

CREATE INDEX idx_daily_logs_completed
ON daily_logs(is_completed);

CREATE INDEX idx_personal_logs_daily_log_id
ON personal_logs(daily_log_id);

CREATE INDEX idx_office_logs_daily_log_id
ON office_logs(daily_log_id);

CREATE INDEX idx_learning_logs_daily_log_id
ON learning_logs(daily_log_id);

CREATE INDEX idx_finance_logs_daily_log_id
ON finance_logs(daily_log_id);

CREATE INDEX idx_food_logs_daily_log_id
ON food_logs(daily_log_id);

CREATE INDEX idx_habit_logs_daily_log_id
ON habit_logs(daily_log_id);