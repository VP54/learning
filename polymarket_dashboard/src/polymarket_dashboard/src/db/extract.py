import logging
from contextlib import contextmanager
import psycopg
from polymarket_dashboard.src.config.db_config import DatabaseConfig
from polymarket_dashboard.src.config.types import Query


@contextmanager
def questdb_cursor(config, *, binary=True):
    with psycopg.connect(
        host=config.host,
        port=config.port,
        user=config.username,
        password=config.password,
        dbname=config.database,
        autocommit=True,
    ) as conn:
        with conn.cursor(binary=binary) as cur:
            yield cur

def extract_data_from_questdb(query: Query, config: DatabaseConfig, logger: logging.Logger, batch_size: int = 1000) -> None:
    """Extract data from Quest DB.

    Args:
        query (Query): DB query to be executed
        config (DatabaseConfig): config to conenct to database
        logger (logging.Logger):
        batch_size: int = 1000
    """

    total_processed = 0
    lst = []
    with questdb_cursor(config) as cur:
        cur.execute(query)

        while True:
            batch = cur.fetchmany(batch_size)
            lst.append(batch)
            if not batch:
                break

            total_processed += len(batch)

            if total_processed % 10_000 == 0:
                logger.info(f"Processed {total_processed} rows so far...")

    logger.info(f"Finished processing {total_processed} total rows")
    return lst


if __name__ == "__main__":
    import logging
    from dotenv import load_dotenv
    load_dotenv("../../../../.env")
    from polymarket_dashboard.src.config.db_config import DatabaseConfig
    db_config = DatabaseConfig(database="polymarket_trades")
    query: Query="SELECT * FROM polymarket_trades LIMIT 10"
    extract_data_from_questdb(config=db_config, query=query, logger=logging.Logger)
