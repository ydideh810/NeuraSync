import ray
import time
import numpy as np

# Initialize Ray
ray.init()

# Simulate AI model with 4 layers
class Model:
    def __init__(self):
        self.layers = [f"Layer {i}" for i in range(4)]

    def forward(self, data):
        """
        Simulate forward pass through model layers
        """
        result = data
        for layer in self.layers:
            result = f"{result} -> {layer}"
            time.sleep(0.5)  # Simulate layer execution time
        return result

@ray.remote
def execute_layer(data, layer_id):
    """
    Parallel execution of individual model layers
    """
    print(f"Running Layer {layer_id}")
    time.sleep(1)  # Simulate processing time
    return f"Layer-{layer_id} Output: {data}"

def parallel_model_execution(data, num_devices=4):
    """
    Splits model into layers and executes them in parallel
    """
    model = Model()

    # Distribute layers to devices
    layer_tasks = [execute_layer.remote(data, i) for i in range(num_devices)]

    # Aggregate results
    results = ray.get(layer_tasks)

    # Combine results into final output
    final_output = " -> ".join(results)
    print(f"Final Model Output: {final_output}")
    return final_output

# Example Usage
if __name__ == "__main__":
    data = "Input Data"
    parallel_model_execution(data)
