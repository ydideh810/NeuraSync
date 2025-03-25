CREATE TABLE fine_tuning_tasks (
    id SERIAL NOT NULL,
    model_name VARCHAR(100) NOT NULL,      
    batch_size INT NOT NULL,               
    learning_rate FLOAT NOT NULL,          
    device_id INT NOT NULL,
    task_status VARCHAR(50) NOT NULL,      
    start_time TIMESTAMP DEFAULT NOW(),
    end_time TIMESTAMP NULL,              
    duration INTERVAL GENERATED ALWAYS AS (end_time - start_time) STORED,
    last_checkpoint TIMESTAMP NULL,
    PRIMARY KEY (id, device_id)
) PARTITION BY HASH (device_id);
