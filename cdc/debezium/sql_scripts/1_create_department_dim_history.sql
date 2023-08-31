CREATE TABLE department_dim_history(
    department_id BIGINT NOT NULL,
    department_description TEXT NOT NULL,
    valid_from TIMESTAMP NOT NULL,
    valid_until TIMESTAMP
);