from fastapi import FastAPI
from models import save_task_history, get_task_history
from pydantic import BaseModel
import random
import time

app = FastAPI()

# API model
class TaskRequest(BaseModel):
    task_id: str
    device_id: str

@app.post("/run-task")
def run_task(task: TaskRequest):
    """
    Simulates task execution and logs to history
    """
    start_time = time.time()

    # Simulate task processing
    execution_time = random.uniform(0.5, 3.0)  # Random exec time
    time.sleep(execution_time)

    # Simulate random success/failure
    status = "Success" if random.random() > 0.2 else "Failed"

    # Store the task in history
    save_task_history(task.task_id, task.device_id, status, execution_time)

    return {
        "task_id": task.task_id,
        "device_id": task.device_id,
        "status": status,
        "execution_time": execution_time
    }

@app.get("/history")
def get_history():
    """
    Fetch historical task execution logs
    """
    history = get_task_history()
    return [{"task_id": t.task_id, 
             "device_id": t.device_id, 
             "status": t.status, 
             "execution_time": t.execution_time, 
             "created_at": t.created_at} 
            for t in history]
