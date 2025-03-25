CREATE TABLE benchmarking (
    id SERIAL NOT NULL,
    device_id INT NOT NULL,
    throughput FLOAT NOT NULL,             
    latency FLOAT NOT NULL,                
    memory_usage FLOAT NOT NULL,           
    cpu_usage FLOAT NOT NULL,              
    gpu_usage FLOAT NOT NULL,              
    timestamp TIMESTAMP NOT NULL,
    PRIMARY KEY (id, timestamp)
) PARTITION BY RANGE (timestamp);
