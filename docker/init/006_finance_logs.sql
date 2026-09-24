-- ==========================================
-- Table: finance_logs
-- Description: Stores daily financial information.
-- ==========================================

CREATE TABLE finance_logs (
    id BIGSERIAL,

    daily_log_id BIGINT NOT NULL,

    daily_expense NUMERIC(10,2),

    income_received NUMERIC(10,2),

    CONSTRAINT pk_finance_logs
        PRIMARY KEY (id),

    CONSTRAINT fk_finance_logs_daily_logs
        FOREIGN KEY (daily_log_id)
        REFERENCES daily_logs(id)
        ON DELETE CASCADE,

    CONSTRAINT uq_finance_logs_daily_log
        UNIQUE (daily_log_id),

    CONSTRAINT chk_daily_expense
        CHECK (
            daily_expense IS NULL
            OR
            daily_expense >= 0
        ),

    CONSTRAINT chk_income_received
        CHECK (
            income_received IS NULL
            OR
            income_received >= 0
        )
);