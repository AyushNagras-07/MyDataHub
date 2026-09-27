-- ==========================================
-- Table: learning_logs
-- Description: Stores learning and project progress.
-- ==========================================

CREATE TABLE learning_logs (
    id BIGSERIAL,

    daily_log_id BIGINT NOT NULL,

    topic_learned TEXT,

    study_hours NUMERIC(4,2),

    project_progress TEXT,

    CONSTRAINT pk_learning_logs
        PRIMARY KEY (id),

    CONSTRAINT fk_learning_logs_daily_logs
        FOREIGN KEY (daily_log_id)
        REFERENCES daily_logs(id)
        ON DELETE CASCADE,

    CONSTRAINT uq_learning_logs_daily_log
        UNIQUE (daily_log_id),

    CONSTRAINT chk_study_hours
        CHECK (
            study_hours IS NULL
            OR
            (study_hours >= 0 AND study_hours <= 24)
        )
);