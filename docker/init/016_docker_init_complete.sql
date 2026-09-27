CREATE TABLE docker_init_complete (
    id INTEGER PRIMARY KEY,
    completed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO docker_init_complete (id)
VALUES (1);