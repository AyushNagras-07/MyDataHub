-- ==========================================
-- Table: personal_logs
-- Description: Stores personal daily information.
-- ==========================================

CREATE TABLE personal_logs (
    id BIGSERIAL,

    daily_log_id BIGINT NOT NULL,

    wake_up_time TIME,

    sleep_time TIME,

    mood SMALLINT,

    special_note TEXT,

    CONSTRAINT pk_personal_logs
        PRIMARY KEY (id),

    CONSTRAINT fk_personal_logs_daily_logs
        FOREIGN KEY (daily_log_id)
        REFERENCES daily_logs(id)
        ON DELETE CASCADE,

    CONSTRAINT uq_personal_logs_daily_log
        UNIQUE (daily_log_id),

    CONSTRAINT chk_personal_logs_mood
        CHECK (mood BETWEEN 1 AND 5)
);