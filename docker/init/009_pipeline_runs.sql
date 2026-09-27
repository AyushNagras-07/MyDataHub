CREATE TABLE pipeline_runs (

    id SERIAL PRIMARY KEY,

    started_at TIMESTAMP NOT NULL,

    completed_at TIMESTAMP,

    total_files INTEGER NOT NULL DEFAULT 0,

    successful_files INTEGER NOT NULL DEFAULT 0,

    failed_files INTEGER NOT NULL DEFAULT 0,

    execution_time DECIMAL(10, 2),

    status VARCHAR(50) NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);