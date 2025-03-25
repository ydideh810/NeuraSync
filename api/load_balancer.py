from fastapi import FastAPI, HTTPException
from redis import Redis
from rq import Queue
import psutil
import time
import random

app = FastAPI()

# Redis connection
redis_conn = Redis(host='localhost', port=6379, db=0)
task_queue = Queue('fine_tune', connection=redis_conn)

# Device status simulation
DEVICE_STATUS = {
    "device1": {"cpu": 20, "gpu": 15, "memory": 30},
    "device2": {"cpu": 40, "gpu": 60, "memory": 50},
    "device3": {"cpu": 10, "gpu": 5, "memory": 20}
}

# Monitor device load
def get_device_load(device_id):
    """
    Simulate real-time device load metrics.
    Replace with actual device monitoring if available.
    """
    return DEVICE_STATUS[device_id]

# Load balancing algorithm
def assign_task(prompt: str, batch_size: int, epochs: int):
    """
    Assigns the fine-tuning task to the least-loaded device.
    """
    # Check device load
    best_device = None
    min_load = float('inf')

    for device, metrics in DEVICE_STATUS.items():
        total_load = metrics["cpu"] + metrics["gpu"] + metrics["memory"]
        
        if total_load < min_load:
            min_load = total_load
            best_device = device

    # Add task to Redis queue
    task_id = f"task-{random.randint(1000, 9999)}"
    task_queue.enqueue("api.fine_tuning.distributed_fine_tune", task_id, prompt, best_device, batch_size, epochs)

    return {
        "task_id": task_id,
        "assigned_device": best_device
    }

# API Endpoint for fine-tuning with load balancing
@app.post("/fine-tune")
def fine_tune(prompt: str, batch_size: int = 4, epochs: int = 3):
    """
    Fine-tuning with automatic load balancing.
    """
    try:
        result = assign_task(prompt, batch_size, epochs)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
