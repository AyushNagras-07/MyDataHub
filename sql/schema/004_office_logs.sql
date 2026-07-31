-- ==========================================
-- Table: office_logs
-- Description: Stores office/work related data.
-- ==========================================

CREATE TABLE office_logs (
    id BIGSERIAL,

    daily_log_id BIGINT NOT NULL,

    hours_worked NUMERIC(4,2),

    main_work_completed TEXT,

    office_learnings TEXT,

    CONSTRAINT pk_office_logs
        PRIMARY KEY (id),

    CONSTRAINT fk_office_logs_daily_logs
        FOREIGN KEY (daily_log_id)
        REFERENCES daily_logs(id)
        ON DELETE CASCADE,

    CONSTRAINT uq_office_logs_daily_log
        UNIQUE (daily_log_id),

    CONSTRAINT chk_hours_worked
        CHECK (
            hours_worked IS NULL
            OR
            (hours_worked >= 0 AND hours_worked <= 24)
        )
);