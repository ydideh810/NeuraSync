from fastapi import FastAPI, WebSocket
from redis import Redis
from sqlalchemy import create_engine, insert, MetaData, Table
import json
import random
import time
import networkx as nx
import matplotlib.pyplot as plt
import asyncio

app = FastAPI()

# Redis and PostgreSQL connections
redis_conn = Redis(host='localhost', port=6379, db=0)
DB_URL = "postgresql://username:password@localhost/neura_sync"
engine = create_engine(DB_URL)
metadata = MetaData()
sharding = Table('model_sharding', metadata, autoload_with=engine)

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

# Simulate sharding data
def generate_sharding_data():
    """
    Simulates layer distribution and communication overhead
    """
    devices = ["device1", "device2", "device3", "device4"]
    layers = [f"Layer-{i}" for i in range(1, 13)]

    data = []
    for layer in layers:
        device = random.choice(devices)
        memory_usage = round(random.uniform(2.0, 6.0), 2)  # GB
        overhead = round(random.uniform(0.1, 1.5), 2)  # GB

        # Store in PostgreSQL
        with engine.connect() as conn:
            stmt = insert(sharding).values(
                layer=layer,
                device=device,
                memory_usage=memory_usage,
                communication_overhead=overhead
            )
            conn.execute(stmt)

        # Send visualization data over WebSockets
        data.append({
            "layer": layer,
            "device": device,
            "memory_usage": memory_usage,
            "communication_overhead": overhead
        })

    return data

# Graph visualization generator
def generate_sharding_graph():
    """
    Generates a tensor sharding graph
    """
    G = nx.Graph()

    devices = ["device1", "device2", "device3", "device4"]
    layers = [f"Layer-{i}" for i in range(1, 13)]

    for layer in layers:
        device = random.choice(devices)
        G.add_node(layer, label=layer)
        G.add_edge(layer, device)

    # Plot graph
    plt.figure(figsize=(12, 8))
    nx.draw(G, with_labels=True, node_color="skyblue", font_size=12)
    plt.savefig("static/sharding_graph.png")
    plt.close()

# Continuous update loop
@app.on_event("startup")
async def update_loop():
    while True:
        data = generate_sharding_data()
        generate_sharding_graph()

        for connection in active_connections:
            await connection.send_text(json.dumps(data))

        await asyncio.sleep(5)
