from fastapi import FastAPI, WebSocket
from redis import Redis
from sqlalchemy import create_engine, insert, MetaData, Table
import torch
import time
import json
import psutil
import GPUtil
import asyncio

app = FastAPI()

# Redis and PostgreSQL connections
redis_conn = Redis(host='localhost', port=6379, db=0)
DB_URL = "postgresql://username:password@localhost/neura_sync"
engine = create_engine(DB_URL)
metadata = MetaData()
benchmarks = Table('benchmarks', metadata, autoload_with=engine)

# WebSocket connections
active_connections = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)

    try:
        while True:
            await asyncio.sleep(1)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        active_connections.remove(websocket)

# Benchmarking Profiler
def get_benchmark_data():
    """
    Gathers real-time system performance metrics
    """
    devices = GPUtil.getGPUs()

    data = []
    
    for device in devices:
        device_name = device.name
        memory_usage = round(device.memoryUtil * 100, 2)  # in %
        gpu_util = round(device.load * 100, 2)  # in %
        cpu_util = psutil.cpu_percent()

        # Simulate latency and throughput metrics
        latency = round(torch.rand(1).item() * 100, 2)  # ms
        throughput = round(torch.rand(1).item() * 500, 2)  # tokens/sec

        # Store in PostgreSQL
        with engine.connect() as conn:
            stmt = insert(benchmarks).values(
                device=device_name,
                throughput=throughput,
                latency=latency,
                memory_usage=memory_usage,
                cpu_utilization=cpu_util,
                gpu_utilization=gpu_util
            )
            conn.execute(stmt)

        # Send data over WebSockets
        data.append({
            "device": device_name,
            "throughput": throughput,
            "latency": latency,
            "memory_usage": memory_usage,
            "cpu_util": cpu_util,
            "gpu_util": gpu_util
        })

    return data

# Continuous benchmark update loop
@app.on_event("startup")
async def benchmark_loop():
    while True:
        data = get_benchmark_data()

        for connection in active_connections:
            await connection.send_text(json.dumps(data))

        await asyncio.sleep(5)
