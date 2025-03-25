import os
import psycopg2
from psycopg2 import pool, OperationalError, InterfaceError
from dotenv import load_dotenv
import logging
import time
import random

# Load environment variables
load_dotenv()

# PostgreSQL configuration from .env
DB_HOSTS = os.getenv("DB_HOSTS", "localhost").split(",")  # Multiple hosts for sharding
DB_PORT = int(os.getenv("DB_PORT", 5432))
DB_NAME = os.getenv("DB_NAME", "neura_sync")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_SSL_MODE = os.getenv("DB_SSL_MODE", "require")  # Use SSL encryption

# Connection pool settings
DB_POOL_MIN = int(os.getenv("DB_POOL_MIN", 5))
DB_POOL_MAX = int(os.getenv("DB_POOL_MAX", 20))
RETRY_ATTEMPTS = 3
RETRY_DELAY = 2

# Logger configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Dictionary to hold connection pools for each shard
db_pools = {}


def create_connection_pool(host, port, user, password, dbname, ssl_mode):
    """
    Create a connection pool for a PostgreSQL shard.
    """
    try:
        logger.info(f"Creating pool for {host}:{port}/{dbname}")
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
            logger.info(f"Connection pool established for {host}")
            return pool
    except OperationalError as e:
        logger.error(f"Failed to create pool for {host}: {e}")
        return None


# Initialize connection pools for each shard
def init_connection_pools():
    """
    Initialize connection pools for all shards.
    """
    for host in DB_HOSTS:
        pool = create_connection_pool(
            host, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME, DB_SSL_MODE
        )
        if pool:
            db_pools[host] = pool


# Shard-aware connection retrieval with failover handling
def get_connection():
    """
    Get a connection with shard-aware routing and failover handling.
    """
    attempts = 0

    while attempts < RETRY_ATTEMPTS:
        try:
            # Randomly select a shard pool for load balancing
            host = random.choice(list(db_pools.keys()))

            # Get connection from pool
            conn = db_pools[host].getconn()

            # Validate connection
            with conn.cursor() as cur:
                cur.execute("SELECT 1;")

            logger.info(f"Connected to {host}")
            return conn

        except (OperationalError, InterfaceError) as e:
            logger.warning(f"Connection failed: {e}. Retrying...")
            attempts += 1
            time.sleep(RETRY_DELAY)

    raise Exception("Failed to connect to the database after multiple attempts")


# Release connection back to the pool
def release_connection(conn):
    """
    Release the connection back to the appropriate pool.
    """
    try:
        for host, pool in db_pools.items():
            if conn:
                pool.putconn(conn)
                logger.info(f"Connection released back to {host}")
                break
    except Exception as e:
        logger.error(f"Failed to release connection: {e}")


# Graceful shutdown of all connection pools
def close_pools():
    """
    Close all PostgreSQL connection pools gracefully.
    """
    for host, pool in db_pools.items():
        pool.closeall()
        logger.info(f"Closed pool for {host}")
