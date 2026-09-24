-- ==========================================
-- Table: habit_logs
-- Description: Stores daily habit information.
-- ==========================================

CREATE TABLE habit_logs (
    id BIGSERIAL,

    daily_log_id BIGINT NOT NULL,

    bath_taken BOOLEAN NOT NULL DEFAULT FALSE,

    hair_washed BOOLEAN NOT NULL DEFAULT FALSE,

    hair_oil_applied BOOLEAN NOT NULL DEFAULT FALSE,

    exercise_done BOOLEAN NOT NULL DEFAULT FALSE,

    pushups SMALLINT,

    reading_pages SMALLINT,

    CONSTRAINT pk_habit_logs
        PRIMARY KEY (id),

    CONSTRAINT fk_habit_logs_daily_logs
        FOREIGN KEY (daily_log_id)
        REFERENCES daily_logs(id)
        ON DELETE CASCADE,

    CONSTRAINT uq_habit_logs_daily_log
        UNIQUE (daily_log_id),

    CONSTRAINT chk_pushups
        CHECK (
            pushups IS NULL
            OR
            (pushups >= 0 AND pushups <= 1000)
        ),

    CONSTRAINT chk_reading_pages
        CHECK (
            reading_pages IS NULL
            OR
            reading_pages >= 0
        )
);