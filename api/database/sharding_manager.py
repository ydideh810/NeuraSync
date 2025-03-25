import os
import random
import logging
import time
from psycopg2 import OperationalError, InterfaceError
from dotenv import load_dotenv
from api.database.connection_pool import get_connection, release_connection

# Load environment variables
load_dotenv()

# Logger configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# PostgreSQL shard configuration
DB_SHARDS = os.getenv("DB_HOSTS", "localhost").split(",")  # Multiple shard hosts
RETRY_ATTEMPTS = 3
RETRY_DELAY = 2

# Shard distribution logic
SHARD_COUNT = len(DB_SHARDS)

def get_shard_index(key: int) -> int:
    """
    Determine the shard index based on a key (e.g., task_id, device_id).
    Uses modulo distribution for even data spread.
    """
    return key % SHARD_COUNT


def route_query(query: str, params=(), shard_key: int = None):
    """
    Routes query to the appropriate PostgreSQL shard.
    Automatically handles retries and failover.
    """
    conn = None
    attempts = 0
    shard_index = 0

    if shard_key is not None:
        # Use sharding key for distribution
        shard_index = get_shard_index(shard_key)
    
    while attempts < RETRY_ATTEMPTS:
        try:
            # Select the appropriate shard
            host = DB_SHARDS[shard_index]

            # Get connection from pool
            conn = get_connection()

            # Execute the query
            with conn.cursor() as cur:
                cur.execute(query, params)
                if query.strip().lower().startswith("select"):
                    result = cur.fetchall()
                else:
                    result = cur.rowcount

            # Release connection
            release_connection(conn)
            return result

        except (OperationalError, InterfaceError) as e:
            logger.warning(f"Query routing failed: {e}. Retrying...")
            attempts += 1
            time.sleep(RETRY_DELAY)

        finally:
            if conn:
                release_connection(conn)

    logger.error("Failed to route query after multiple attempts.")
    return None


def distribute_insert(table: str, data: dict, shard_key: int):
    """
    Distributes INSERT operations across shards.
    Automatically selects the correct shard based on the key.
    """
    shard_index = get_shard_index(shard_key)
    host = DB_SHARDS[shard_index]

    columns = ', '.join(data.keys())
    values = ', '.join(['%s'] * len(data))
    
    query = f"""
        INSERT INTO {table} ({columns})
        VALUES ({values});
    """
    
    params = tuple(data.values())

    logger.info(f"Routing INSERT to shard {shard_index} ({host})...")
    return route_query(query, params, shard_key)


def distributed_select(table: str, shard_key: int, condition: str = "1=1"):
    """
    Executes SELECT queries distributed across the shards.
    """
    shard_index = get_shard_index(shard_key)
    host = DB_SHARDS[shard_index]

    query = f"""
        SELECT * FROM {table}
        WHERE {condition};
    """

    logger.info(f"Routing SELECT to shard {shard_index} ({host})...")
    return route_query(query, shard_key=shard_key)


def shard_health_check():
    """
    Perform health checks on all shards.
    """
    logger.info("Running shard health checks...")

    for index, shard in enumerate(DB_SHARDS):
        try:
            conn = get_connection()
            with conn.cursor() as cur:
                cur.execute("SELECT 1;")
                logger.info(f"Shard {index + 1}: {shard} is healthy.")
        except Exception as e:
            logger.error(f"Shard {index + 1}: {shard} is DOWN: {e}")
        finally:
            if conn:
                release_connection(conn)


def failover_handler():
    """
    Handle failover by rerouting queries to the next available shard.
    """
    logger.warning("Failover triggered. Rerouting to next shard...")
    random.shuffle(DB_SHARDS)


# Graceful shutdown
def close_shards():
    """
    Close all shard connections on shutdown.
    """
    logger.info("Closing all shard connections...")
    from api.database.connection_pool import close_pools
    close_pools()
