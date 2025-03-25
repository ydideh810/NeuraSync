from fastapi import FastAPI, WebSocket
from redis import Redis
from sqlalchemy import create_engine, insert, MetaData, Table
import json
import time
import random
import asyncio

app = FastAPI()

# Redis connection
redis_conn = Redis(host='localhost', port=6379, db=0)

# PostgreSQL connection
DB_URL = "postgresql://username:password@localhost/neura_sync"
engine = create_engine(DB_URL)
metadata = MetaData()
failures = Table('task_failures', metadata, autoload_with=engine)

# WebSockets for real-time updates
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

# Simulate device failure
def simulate_failure():
    """
    Simulates device failure for testing purposes.
    """
    devices = ["device1", "device2", "device3"]
    failed_device = random.choice(devices)

    # Log failure in PostgreSQL
    with engine.connect() as conn:
        stmt = insert(failures).values(
            task_id=f"task-{random.randint(1000, 9999)}",
            status="FAILED",
            device=failed_device
        )
        conn.execute(stmt)

    # Trigger recovery
    recovery_task = {
        "task_id": f"task-{random.randint(1000, 9999)}",
        "status": "RECOVERED",
        "device": random.choice([d for d in devices if d != failed_device])
    }

    asyncio.create_task(send_recovery_event(recovery_task))

# Send recovery event via WebSockets
async def send_recovery_event(task):
    """
    Sends recovery event to all active WebSocket connections.
    """
    for connection in active_connections:
        await connection.send_text(json.dumps(task))

# Recovery loop
@app.on_event("startup")
async def recovery_loop():
    while True:
        simulate_failure()
        await asyncio.sleep(5)
