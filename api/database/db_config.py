import os
import psycopg2
from psycopg2 import pool, OperationalError, InterfaceError
from dotenv import load_dotenv
import time
import random
import logging

# Load environment variables from .env
load_dotenv()

# PostgreSQL Configuration (Environment Variables)
DB_HOSTS = os.getenv("DB_HOSTS", "localhost").split(",")  # Multiple hosts for replication
DB_PORT = int(os.getenv("DB_PORT", 5432))
DB_NAME = os.getenv("DB_NAME", "neura_sync")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_SSL_MODE = os.getenv("DB_SSL_MODE", "require")  # Enforce SSL
DB_POOL_MIN = int(os.getenv("DB_POOL_MIN", 5))
DB_POOL_MAX = int(os.getenv("DB_POOL_MAX", 20))
RETRY_ATTEMPTS = 3
RETRY_DELAY = 2

# Logger configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Connection Pool Initialization
db_pools = {}

def create_connection_pool(host, port, user, password, dbname, ssl_mode):
    """
    Create a connection pool for PostgreSQL.
    """
    try:
        logger.info(f"Connecting to {host}:{port}/{dbname}...")
        pool = psycopg2.pool.SimpleConnectionPool(
            DB_POOL_MIN, DB_POOL_MAX,
            host=host,
            port=port,
            user=user,
            password=password,
            dbname=dbname,
            sslmode=ssl_mode
        )
        if pool:
            logger.info(f"Connected to {host}.")
            return pool
    except OperationalError as e:
        logger.error(f"Failed to connect to {host}: {e}")
        return None

# Initialize Connection Pools for Shards (Replication Support)
for host in DB_HOSTS:
    pool = create_connection_pool(
        host, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME, DB_SSL_MODE
    )
    if pool:
        db_pools[host] = pool

# Failover & Retry Logic
def get_connection():
    """
    Get a connection with failover and retry logic.
    """
    attempts = 0

    while attempts < RETRY_ATTEMPTS:
        try:
            # Randomly choose a pool to distribute connections evenly
            host = random.choice(list(db_pools.keys()))
            
            # Get a connection from the pool
            conn = db_pools[host].getconn()

            # Validate the connection
            with conn.cursor() as cur:
                cur.execute("SELECT 1;")

            logger.info(f"Connected to {host}")
            return conn

        except (OperationalError, InterfaceError) as e:
            logger.warning(f"Connection failed: {e}. Retrying...")
            attempts += 1
            time.sleep(RETRY_DELAY)

    raise Exception("Failed to connect to database after multiple attempts")

# Release the connection back to the pool
def release_connection(conn):
    """
    Release the connection back to the pool.
    """
    try:
        for host, pool in db_pools.items():
            if conn:
                pool.putconn(conn)
                logger.info(f"Connection released to {host}")
    except Exception as e:
        logger.error(f"Failed to release connection: {e}")

# Graceful Pool Cleanup
def close_pools():
    """
    Close all connection pools.
    """
    for host, pool in db_pools.items():
        pool.closeall()
        logger.info(f"Closed pool for {host}")
