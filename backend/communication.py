import grpc
import communication_pb2
import communication_pb2_grpc
import numpy as np

# Simulate shard distribution
def distribute_shards(tensor, devices):
    """
    Splits tensor and sends shards to devices
    """
    shard_size = len(tensor) // len(devices)
    shards = [tensor[i * shard_size:(i + 1) * shard_size] for i in range(len(devices))]

    # Send shards to devices
    for i, device in enumerate(devices):
        channel = grpc.insecure_channel(device['ip'] + ":50051")
        stub = communication_pb2_grpc.CommunicationStub(channel)

        request = communication_pb2.TaskRequest(
            device_id=device['name'],
            data=shards[i].tobytes()
        )
        response = stub.SendTask(request)

        print(f"Sent shard to {device['name']} - Response: {response.message}")

# Example Usage
if __name__ == "__main__":
    tensor = np.random.rand(10000)
    devices = [
        {"name": "Device-1", "ip": "127.0.0.1"},
        {"name": "Device-2", "ip": "127.0.0.2"},
        {"name": "Device-3", "ip": "127.0.0.3"},
        {"name": "Device-4", "ip": "127.0.0.4"},
    ]

    distribute_shards(tensor, devices)
