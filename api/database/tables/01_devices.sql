CREATE TABLE devices (
    id SERIAL PRIMARY KEY,
    device_name VARCHAR(100) NOT NULL,
    device_type VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL,           -- (Active, Idle, Failed)
    total_memory FLOAT,                     
    memory_used FLOAT,                      
    memory_utilization FLOAT,               
    cpu_utilization FLOAT,                  
    gpu_utilization FLOAT,                  
    temperature FLOAT,                      
    last_updated TIMESTAMP DEFAULT NOW()
);
