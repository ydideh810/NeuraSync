CREATE TABLE failure_recovery (
    id SERIAL PRIMARY KEY,
    device_id INT REFERENCES devices(id) ON DELETE CASCADE,
    failure_time TIMESTAMP DEFAULT NOW(),
    recovery_time TIMESTAMP NULL,
    recovery_status VARCHAR(50) NOT NULL,  
    error_log TEXT                         
);
