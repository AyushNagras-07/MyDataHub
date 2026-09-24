-- ==========================================
-- Table: food_logs
-- Description: Stores daily food information.
-- ==========================================

CREATE TABLE food_logs (
    id BIGSERIAL,

    daily_log_id BIGINT NOT NULL,

    breakfast TEXT,

    lunch TEXT,

    dinner TEXT,

    tea_coffee_count SMALLINT,

    CONSTRAINT pk_food_logs
        PRIMARY KEY (id),

    CONSTRAINT fk_food_logs_daily_logs
        FOREIGN KEY (daily_log_id)
        REFERENCES daily_logs(id)
        ON DELETE CASCADE,

    CONSTRAINT uq_food_logs_daily_log
        UNIQUE (daily_log_id),

    CONSTRAINT chk_tea_coffee_count
        CHECK (
            tea_coffee_count IS NULL
            OR
            (tea_coffee_count >= 0 AND tea_coffee_count <= 20)
        )
);