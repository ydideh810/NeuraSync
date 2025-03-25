import ray
import time
import numpy as np

# Initialize Ray
ray.init()

@ray.remote
def execute_task(task_id, data):
    """
    Executes a distributed task in parallel
    """
    print(f"Executing task {task_id} on device")
    time.sleep(1)  # Simulate AI processing
    return f"Task {task_id} result: {np.sum(data)}"

def distribute_tasks(tasks):
    """
    Distributes tasks across multiple devices
    """
    task_refs = [execute_task.remote(i, np.random.rand(1000)) for i in range(tasks)]
    results = ray.get(task_refs)
    
    for result in results:
        print(result)

if __name__ == "__main__":
    distribute_tasks(5)
