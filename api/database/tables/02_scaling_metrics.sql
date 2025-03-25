CREATE TABLE scaling_metrics (
    id SERIAL NOT NULL,
    device_id INT NOT NULL,
    action VARCHAR(50) NOT NULL,           -- (SCALE_UP, SCALE_DOWN)
    utilization FLOAT NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    PRIMARY KEY (id, timestamp)
) PARTITION BY RANGE (timestamp);
