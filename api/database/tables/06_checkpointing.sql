CREATE TABLE checkpointing (
    id SERIAL NOT NULL,
    task_id INT NOT NULL,
    model_name VARCHAR(100) NOT NULL,
    checkpoint_path VARCHAR(255) NOT NULL,
    saved_time TIMESTAMP NOT NULL,
    PRIMARY KEY (id, task_id)
) PARTITION BY HASH (task_id);
