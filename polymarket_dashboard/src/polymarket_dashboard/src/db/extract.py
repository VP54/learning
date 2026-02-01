import psycopg
from polymarket_dashboard.src.config.types import Query


def extract_data_from_questdb(query: Query, config, logger, batch_size: int=1000):
    with psycopg.connect(
            host=config.host,
            port=config.port,
            user=config.user,
            password=config.password,
            dbname=config.dbname,
            autocommit=True
    ) as conn:
        with conn.cursor(binary=True) as cur:
            cur.execute(query)
            batch_size = batch_size
            total_processed = 0
            while True:
                batch = cur.fetchmany(batch_size)
                if not batch:
                    break
                total_processed += len(batch)
                if total_processed % 10000 == 0:
                    logger.info(f"Processed {total_processed} rows so far...")

            logger.info(f"Finished processing {total_processed} total rows")
    return batch