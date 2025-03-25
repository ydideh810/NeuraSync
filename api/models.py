from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# PostgreSQL connection string
DATABASE_URL = "postgresql://neura_user:password@localhost/neura_sync"

# Initialize SQLAlchemy
Base = declarative_base()
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

# Task history model
class TaskHistory(Base):
    __tablename__ = "task_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(String, unique=True, nullable=False)
    device_id = Column(String, nullable=False)
    status = Column(String, nullable=False)
    execution_time = Column(Float)
    created_at = Column(DateTime, default=func.now())

# Create tables
Base.metadata.create_all(engine)

# Save a task record
def save_task_history(task_id, device_id, status, execution_time):
    session = Session()
    new_task = TaskHistory(
        task_id=task_id,
        device_id=device_id,
        status=status,
        execution_time=execution_time
    )
    session.add(new_task)
    session.commit()
    session.close()

# Get historical tasks
def get_task_history():
    session = Session()
    history = session.query(TaskHistory).order_by(TaskHistory.created_at.desc()).all()
    session.close()
    return history
