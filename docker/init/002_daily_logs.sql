-- ==========================================
-- Table: daily_logs
-- Description: Stores one daily log per user.
-- ==========================================

CREATE TABLE daily_logs (
    id BIGSERIAL PRIMARY KEY,

    user_id BIGINT NOT NULL,

    log_date DATE NOT NULL,

    is_completed BOOLEAN NOT NULL DEFAULT FALSE,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_daily_logs_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    CONSTRAINT uq_user_log_date
        UNIQUE (user_id, log_date)
);