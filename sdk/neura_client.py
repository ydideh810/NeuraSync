import requests

class NeuraClient:
    def __init__(self, server_url):
        self.server_url = server_url

    def run_task(self, task_data):
        response = requests.post(f"{self.server_url}/task", json=task_data)
        return response.json()

# Example usage
client = NeuraClient("http://localhost:8000")
print(client.run_task({"task": "LLM inference"}))
