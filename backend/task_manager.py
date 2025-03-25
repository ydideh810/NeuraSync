import threading
import time

# Simulate distributed tasks
tasks = {}
task_id = 0

def execute_task(task):
    """
    Simulates task execution
    """
    global task_id
    task_id += 1
    print(f"Running task {task_id} on device")
    time.sleep(2)  # Simulate execution time
    tasks[task_id] = "Success"
    return f"Task {task_id} executed"

def failover_handler():
    """
    Monitors and redistributes failed tasks
    """
    while True:
        time.sleep(5)
        for task_id, status in list(tasks.items()):
            if status != "Success":
                print(f"Failover triggered for task {task_id}")
                execute_task(task_id)

# Start task execution and failover handler
threading.Thread(target=failover_handler).start()

# Simulate workload
for _ in range(3):
    threading.Thread(target=execute_task, args=("Task",)).start()
