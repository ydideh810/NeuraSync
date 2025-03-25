from fastapi import FastAPI, HTTPException
from redis import Redis
from rq import Queue
import torch
import os
import time
from sqlalchemy import create_engine, MetaData, Table, insert
from models import save_task_history

app = FastAPI()

# Redis and PostgreSQL connections
redis_conn = Redis(host='localhost', port=6379, db=0)
task_queue = Queue('fine_tune', connection=redis_conn)

# PostgreSQL connection
DB_URL = "postgresql://username:password@localhost/neura_sync"
engine = create_engine(DB_URL)
metadata = MetaData()
checkpoints = Table('checkpoints', metadata, autoload_with=engine)

# Directory to store model checkpoints
CHECKPOINT_DIR = "./checkpoints"
os.makedirs(CHECKPOINT_DIR, exist_ok=True)

# Save checkpoint function
def save_checkpoint(model, task_id):
    """
    Save model checkpoint with task ID
    """
    checkpoint_path = f"{CHECKPOINT_DIR}/{task_id}_checkpoint.pt"
    torch.save(model.state_dict(), checkpoint_path)

    # Store checkpoint metadata in PostgreSQL
    with engine.connect() as conn:
        stmt = insert(checkpoints).values(
            task_id=task_id,
            model_path=checkpoint_path
        )
        conn.execute(stmt)

    return checkpoint_path

# Restore checkpoint function
def restore_checkpoint(model, task_id):
    """
    Restore model from last saved checkpoint
    """
    with engine.connect() as conn:
        result = conn.execute(
            checkpoints.select().where(checkpoints.c.task_id == task_id)
        ).fetchone()

    if result:
        checkpoint_path = result['model_path']
        model.load_state_dict(torch.load(checkpoint_path))
        return model
    else:
        raise FileNotFoundError("No checkpoint found.")

# Fault recovery function
def recover_from_failure(task_id, model):
    """
    Recover fine-tuning from last checkpoint
    """
    try:
        model = restore_checkpoint(model, task_id)
        print(f"Resuming fine-tuning from checkpoint {task_id}")
        return model
    except Exception as e:
        print(f"Failed to restore checkpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

