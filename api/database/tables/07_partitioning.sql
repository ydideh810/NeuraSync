-- Partitioning logic
CREATE TABLE scaling_metrics_2025_q1  
    PARTITION OF scaling_metrics  
    FOR VALUES FROM ('2025-01-01') TO ('2025-04-01');

CREATE TABLE fine_tuning_tasks_part_1  
    PARTITION OF fine_tuning_tasks  
    FOR VALUES WITH (MODULUS 4, REMAINDER 0);
