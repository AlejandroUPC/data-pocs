CREATE TABLE department_dim(
       department_id BIGINT NOT NULL,
       department_description TEXT NOT NULL,
       created_at TIMESTAMP DEFAULT NOW(),
       updated_at TIMESTAMP DEFAULT NOW(),
       PRIMARY KEY(department_id)
);
ALTER TABLE department_dim REPLICA IDENTITY FULL;