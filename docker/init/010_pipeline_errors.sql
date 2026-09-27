CREATE TABLE pipeline_errors (
    id BIGSERIAL,

    pipeline_run_id BIGINT NOT NULL,

    file_name VARCHAR(255) NOT NULL,

    stage VARCHAR(50),

    error_type VARCHAR(100),

    error_message TEXT NOT NULL,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_pipeline_errors
        PRIMARY KEY (id),

    CONSTRAINT fk_pipeline_errors_pipeline_runs
        FOREIGN KEY (pipeline_run_id)
        REFERENCES pipeline_runs(id)
        ON DELETE CASCADE,

    CONSTRAINT chk_pipeline_errors_stage
        CHECK (
            stage IS NULL OR
            UPPER(stage) IN (
                'EXTRACT',
                'VALIDATION',
                'TRANSFORMATION',
                'LOAD'
            )
        )
);