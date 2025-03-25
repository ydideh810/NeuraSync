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
scaling_metrics = Table('scaling_metrics', metadata, autoload_with=engine)

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

# Auto-scaling and rebalancing logic
def monitor_resources():
    devices = GPUtil.getGPUs()

    scaling_actions = []

    for device in devices:
        device_name = device.name
        memory_usage = round(device.memoryUtil * 100, 2)  # %
        gpu_util = round(device.load * 100, 2)  # %
        cpu_util = psutil.cpu_percent()

        # Auto-scaling triggers
        if cpu_util > 85 or memory_usage > 90:
            action = "SCALE_UP"
            scaling_actions.append((device_name, action))

        elif cpu_util < 20 and memory_usage < 30:
            action = "SCALE_DOWN"
            scaling_actions.append((device_name, action))

        else:
            action = "STABLE"

        # Store scaling action in PostgreSQL
        with engine.connect() as conn:
            stmt = insert(scaling_metrics).values(
                action=action,
                device=device_name,
                utilization=memory_usage
            )
            conn.execute(stmt)

    return scaling_actions

# Rebalancing logic
def rebalance_tasks():
    """
    Redistributes tasks if devices are overloaded or idle.
    """
    devices = GPUtil.getGPUs()

    for device in devices:
        memory_usage = round(device.memoryUtil * 100, 2)
        if memory_usage > 90:
            # Redistribute tasks
            print(f"Rebalancing: {device.name} is overloaded. Redistributing tasks...")

# Continuous monitoring and scaling loop
@app.on_event("startup")
async def scaling_loop():
    while True:
        actions = monitor_resources()
        rebalance_tasks()

        # Send metrics to frontend
        for connection in active_connections:
            await connection.send_text(json.dumps(actions))

        await asyncio.sleep(5)
