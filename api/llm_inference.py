from fastapi import FastAPI, HTTPException
from llama_cpp import Llama
from models import save_task_history, get_task_history
import redis
import time
import random

app = FastAPI()

# Redis connection
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Load LLM models
MODEL_PATH = "./models/mixtral-8x7b-instruct-v0.1.Q4_K_M.gguf"  # Change path for Llama 3
llm = Llama(model_path=MODEL_PATH, n_ctx=4096, n_threads=8)

# Distributed inference function
def distributed_inference(prompt: str, devices: list):
    """
    Distributes inference tasks across multiple devices.
    """
    num_devices = len(devices)
    shard_size = len(prompt) // num_devices
    results = []

    for i, device in enumerate(devices):
        start_idx = i * shard_size
        end_idx = (i + 1) * shard_size if i < num_devices - 1 else len(prompt)
        
        # Simulate parallel execution
        partial_prompt = prompt[start_idx:end_idx]

        # Execute inference on the device
        output = llm(f"{partial_prompt}")["choices"][0]["text"]
        results.append(output)

    return "".join(results)

# Inference endpoint
@app.post("/infer")
def infer(prompt: str):
    """
    Distributed inference across NEURA-SYNC devices.
    """
    start_time = time.time()

    # Get device list from Redis
    devices = redis_client.lrange("devices", 0, -1)
    if not devices:
        raise HTTPException(status_code=500, detail="No devices available")

    # Perform distributed inference
    output = distributed_inference(prompt, devices)

    execution_time = time.time() - start_time

    # Store results in PostgreSQL
    task_id = f"task-{random.randint(1000, 9999)}"
    save_task_history(task_id, device_id="distributed", status="Success", execution_time=execution_time)

    return {
        "task_id": task_id,
        "output": output,
        "execution_time": execution_time
    }
